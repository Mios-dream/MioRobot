"""
qwen模型的自动加载方法
可以自动加载model和tokenizer
也支持加载lora
使用时需要根据具体情况进行修改。
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoModel,
    BitsAndBytesConfig,
)
from peft import PeftModel


from typing import TYPE_CHECKING, Tuple


class Log:
    """
    简单的日志类
    包含三个方法: infor, warning, error
    """

    @staticmethod
    def info(msg):
        print("信息:", msg)

    @staticmethod
    def warning(msg):
        print("警告:", msg)

    @staticmethod
    def error(msg):
        print("错误:", msg)


if TYPE_CHECKING:
    from transformers import PreTrainedModel, PreTrainedTokenizer


def load_adapter(model, lora_path_list: list[str]):
    """
    @due 这个方法用于给模型添加Lora，支持多个lora加载
    @param
        model: 需要添加的模型
        lora_path: 需要加载的lora的路径列表
    @return 加载lora后的模型

    """

    Log.info("加载的适配器类型: LoRA")

    for adapter in lora_path_list:

        model = PeftModel.from_pretrained(model, adapter)

        model = model.merge_and_unload()

    if len(lora_path_list) > 0:

        Log.info(f"混合了 {len(lora_path_list)} 个适配器.")

    return model


def load_model(model_path: str, device: str = "cuda") -> "PreTrainedModel":
    """

    @due 加载llm模型
    @param
        model_name:加载模型的路径
        device:将模型加载到的设备，默认为cuda
    @return 模型对象


    """
    torch_dtype = torch.float16  # 加载模型精度，默认float16 ,可选float32或混合精度

    # 加载参数
    params = {"trust_remote_code": True, "low_cpu_mem_usage": True}

    # 量化方法
    # quantization_config_params = {
    #     "load_in_4bit": True,
    #     "bnb_4bit_compute_dtype": torch.float16,
    #     "bnb_4bit_quant_type": "nf4",
    #     "bnb_4bit_use_double_quant": False,
    # }
    # params["quantization_config"] = BitsAndBytesConfig(**quantization_config_params)

    # qwen用这个加载
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch_dtype, trust_remote_code=True
    ).to(device)

    # chatglm2用这个加载
    # model = AutoModel.from_pretrained(model_path,torch_dtype=torch_dtype, **params).to(device)

    return model


def load_tokenizer(model_path: str) -> "PreTrainedTokenizer":
    """
    @due 加载模型的tokenizer
    @param
        model_name:tokenizer的路径
    @return
    """
    return AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)


def auto_load_model(model_path: str) -> Tuple["PreTrainedModel", "PreTrainedTokenizer"]:
    """
    @due 模型的快捷加载方法
    @param
        model_path:需要加载的模型路径
    @return model和tokenizer对象
    """

    model = load_model(model_path)
    tokenizer = load_tokenizer(model_path)
    return model, tokenizer


def main():

    model, tokenizer = auto_load_model(
        "D:/yutuber_ai/mio_ai/models/qwen/Qwen1___5-4B-Chat"
    )

    prompt = "你叫什么名字"
    messages = [
        {"role": "system", "content": "你的名字叫小澪,是澪之梦工作室的一个看板娘"},
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to("cuda")

    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    # 模型的回复
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    print(response)

    torch.cuda.empty_cache()  # 在不再需要模型数据时清理缓存


if __name__ == "__main__":
    main()
