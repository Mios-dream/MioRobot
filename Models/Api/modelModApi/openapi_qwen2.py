import time
import torch
import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Literal, Optional, Union
from sse_starlette.sse import EventSourceResponse
from Models.Api.modelModApi import auto_mode_qwen
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import PolynomialFeatures
import tiktoken
import numpy as np
from transformers import TextIteratorStreamer
from threading import Thread


@asynccontextmanager
async def lifespan(app: FastAPI):  # collects GPU memory
    """异步上下文管理器 lifespan，用于清零CUDA缓存"""
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # 来清空 CUDA 缓存，释放 GPU 内存
        torch.cuda.ipc_collect()


app = FastAPI(
    lifespan=lifespan
)  # 通过将 lifespan 上下文管理器传递给 FastAPI 的构造函数，可以在 FastAPI 应用程序的
# 生命周期中管理 GPU 资源，并确保在每个请求处理完成后执行必要的清理操作

app.add_middleware(  # 使用 add_middleware 方法向 FastAPI 应用程序添加中间件
    CORSMiddleware,
    allow_origins=["*"],  #
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 参数说明：
# CORSMiddleware：指定要添加的中间件类。 CORSMiddleware是用于处理跨域资源共享（CORS）的中间件。CORS 是一种机制，允许在浏览器中运行的 Web 应用程序访问不同域上的资源。CORSMiddleware 中间件帮助管理跨域请求，并设置相应的 CORS 标头
# allow_origins=["*"]：允许的源（域）列表。在这个例子中，设置为 ["*"] 表示允许来自任何源的请求。
# allow_credentials=True：指示是否允许发送凭据（如 cookies）的请求。
# allow_methods=["*"]：允许的 HTTP 方法列表。在这个例子中，设置为 ["*"] 表示允许所有的 HTTP 方法。
# allow_headers=["*"]：允许的请求标头列表。在这个例子中，设置为 ["*"] 表示允许所有的请求标头。


# 定义 ModelCard 数据模型，如model_card = ModelCard(id="123", owned_by="John")，print(model_card.id)  # 输出: 123
class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"
    root: Optional[str] = None
    parent: Optional[str] = None
    permission: Optional[list] = None


# 定义 ModelList 数据模型
class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


# 定义ChatMessage 数据模型
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


# 定义DeltaMessage 数据模型-->存储流式是输出的对话
class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None


# 定义ChatCompletionRequest 数据模型-->储存ChatCompletion的Request
class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_length: Optional[int] = None
    stream: Optional[bool] = (
        False  # 当在ChatGPT API请求中设置stream为True时，API将会以流式的方式生成聊天响应。
    )
    # 这意味着API会逐步生成聊天文本，并将其以流（stream）的形式发送给客户端。
    # 客户端可以从流中逐步读取响应，而不需要等待完整的响应返回


# 定义ChatCompletionResponseChoice 数据模型-->储存ChatCompletionResponse的Choice
class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


# 定义ChatCompletionResponseStreamChoice数据模型-->储存ChatCompletionResponseStream的Choice
class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]]


# 定义ChatCompletionResponse数据模型-->储存ChatCompletionResponse的类型
class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[
        Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]
    ]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))


# 这段代码定义了一个路由处理函数 list_models()，用于处理针对路径 "/v1/models" 的 HTTP GET 请求。
# 在该函数中，创建一个 ModelCard 对象，并将其添加到 ModelList 对象中作为响应返回。
@app.get("/v1/models", response_model=ModelList)
async def list_models():
    global model_args
    model_card = ModelCard(id="chatglm2")
    return ModelList(data=[model_card])


# 路径："/v1/chat/completions"，响应模型：ChatCompletionResponse
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    global model, tokenizer

    # 限制只能以用户身份提问
    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Invalid request")
    # 获取messages的content
    # 获取用户新的消息
    query = request.messages[-1].content

    # 获取历史消息并判断是否为system message，然后将system message与最新的message组合
    prev_messages = request.messages[:-1]

    history = []
    if len(prev_messages) > 0 and prev_messages[0].role == "system":

        # 系统消息
        # prev_messages.pop(0) 的作用是移除 prev_messages 列表中索引位置为 0 的元素，并返回该元素的值。同时，由于该元素是从列表中移除的， prev_messages 列表的长度会减少一个元素。
        history.append({"role": "system", "content": prev_messages.pop(0).content})
    # 将每次的"user"提问和"assistant"回答打包依次储存为history（由于prev_messages.pop(0)，这里已经没有了system ）

    if len(prev_messages) % 2 == 0:  # 确定prev_messages中除了system message还有其他消息
        for i in range(0, len(prev_messages), 2):
            if (
                prev_messages[i].role == "user"
                and prev_messages[i + 1].role == "assistant"
            ):
                # history.append([prev_messages[i].content, prev_messages[i + 1].content])
                history.append(
                    {"role": "assistant", "content": prev_messages[i + 1].content}
                )
                history.append({"role": "user", "content": prev_messages[i].content})

    if request.stream:  # 如何流式输出为True
        generate = predict(query, history, request.model)  # 返回流式输出的结果
        return EventSourceResponse(
            generate, media_type="text/event-stream"
        )  # 使用 EventSourceResponse 类来构造响应对象。
        # 客户端可以通过订阅该响应对象以接收服务器发送的事件流
    # 如果不是流式输出则直接输出全部response,

    history.append({"role": "user", "content": query})

    text = tokenizer.apply_chat_template(
        history, tokenize=False, add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to("cuda")

    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    # 模型的回复
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=response),
        finish_reason="stop",
    )

    return ChatCompletionResponse(
        model=request.model, choices=[choice_data], object="chat.completion"
    )


async def predict(query: str, history: List[List[str]], model_id: str):
    global model, tokenizer

    # 定义流式输出的设置
    choice_data = ChatCompletionResponseStreamChoice(
        index=0, delta=DeltaMessage(role="assistant"), finish_reason=None
    )
    # 将流式输出以ChatCompletionResponse数据模型储存
    chunk = ChatCompletionResponse(
        model=model_id, choices=[choice_data], object="chat.completion.chunk"
    )
    yield "{}".format(chunk.model_dump_json())  # 使用yield进行流式输出

    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    history.append({"role": "user", "content": query})

    print(history)

    text = tokenizer.apply_chat_template(
        history, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to("cuda")

    # Directly use generate() and tokenizer.decode() to get the output.
    # Use `max_new_tokens` to control the maximum output length.
    # generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
    # generated_ids = [
    #     output_ids[len(input_ids) :]
    #     for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    # ]

    generation_kwargs = dict(model_inputs, streamer=streamer, max_new_tokens=512)

    thread = Thread(target=model.generate, kwargs=generation_kwargs)

    thread.start()
    # for new_response in streamer:
    #     if (
    #         len(new_response) == current_length
    #     ):  # 如果新响应的长度与当前长度相等，说明没有新的文本生成，继续下一次循环
    #         continue

    #     new_text = new_response[current_length:]  # 获取新增的文本部分
    #     current_length = len(new_response)
    new_text = ""
    for new_response in streamer:

        # if len(new_response) == current_length:
        #     continue

        new_text = new_response
        # current_length = len(new_response)
        # 将流式输出的内容-->ChatCompletionResponseStreamChoice
        choice_data = ChatCompletionResponseStreamChoice(
            index=0, delta=DeltaMessage(content=new_text), finish_reason=None
        )
        # 实时返回输出内容
        chunk = ChatCompletionResponse(
            model=model_id, choices=[choice_data], object="chat.completion.chunk"
        )
        yield "{}".format(chunk.model_dump_json())

    # 全部输出后返回'[DONE]'
    choice_data = ChatCompletionResponseStreamChoice(
        index=0, delta=DeltaMessage(), finish_reason="stop"
    )
    chunk = ChatCompletionResponse(
        model=model_id, choices=[choice_data], object="chat.completion.chunk"
    )
    yield "{}".format(chunk.model_dump_json())
    yield "[DONE]"


class EmbeddingRequest(BaseModel):
    input: List[str]
    model: str


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def expand_features(embedding, target_length):
    poly = PolynomialFeatures(degree=2)
    expanded_embedding = poly.fit_transform(embedding.reshape(1, -1))
    expanded_embedding = expanded_embedding.flatten()
    if len(expanded_embedding) > target_length:
        # 如果扩展后的特征超过目标长度，可以通过截断或其他方法来减少维度
        expanded_embedding = expanded_embedding[:target_length]
    elif len(expanded_embedding) < target_length:
        # 如果扩展后的特征少于目标长度，可以通过填充或其他方法来增加维度
        expanded_embedding = np.pad(
            expanded_embedding, (0, target_length - len(expanded_embedding))
        )
    return expanded_embedding


# 实现文本分割功能
@app.post("/v1/embeddings")
async def get_embeddings(request: EmbeddingRequest):
    # 计算嵌入向量和tokens数量
    embeddings = [embeddings_model.encode(text) for text in request.input]

    # 如果嵌入向量的维度不为1536，则使用插值法扩展至1536维度
    embeddings = [
        expand_features(embedding, 1536) if len(embedding) < 1536 else embedding
        for embedding in embeddings
    ]

    # Min-Max normalization 归一化
    embeddings = [embedding / np.linalg.norm(embedding) for embedding in embeddings]

    # 将numpy数组转换为列表
    embeddings = [embedding.tolist() for embedding in embeddings]
    prompt_tokens = sum(len(text.split()) for text in request.input)
    total_tokens = sum(num_tokens_from_string(text) for text in request.input)

    response = {
        "data": [
            {"embedding": embedding, "index": index, "object": "embedding"}
            for index, embedding in enumerate(embeddings)
        ],
        "model": request.model,
        "object": "list",
        "usage": {
            "prompt_tokens": prompt_tokens,
            "total_tokens": total_tokens,
        },
    }

    return response


model_path = "D:/Qwen-7B/Qwen1.5-4B-Chat"
# model_path = "/root/autodl-tmp/LLaMA-Factory/mode/ZhipuAI/chatglm2-6b"

embeddings_model_path = "/root/autodl-tmp/LLaMA-Factory/mode/xrunda/m3e-base"

model, tokenizer = auto_mode_qwen.auto_load_model(model_path)
# 多显卡支持，使用下面两行代替上面一行，将num_gpus改为你实际的显卡数量
# from utils import load_model_on_gpus
# model = load_model_on_gpus("THUDM/chatglm2-6b", num_gpus=2)

# 是否给模型添加lora
is_loder_lora = False
# 是否加载m3e模型
is_loder_m3e = False
if is_loder_lora:
    # lora路径
    adapter_path = []
    for adapter in adapter_path:
        model = auto_mode_qwen.load_adapter(model, adapter)

if is_loder_m3e:
    embeddings_model = SentenceTransformer(embeddings_model_path, device="cuda")

model.eval()
