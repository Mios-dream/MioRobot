from torchvision.transforms import functional
import sys

# 兼容库中旧代码使用
sys.modules["torchvision.transforms.functional_tensor"] = functional

import asyncio
import numpy as np
from io import BytesIO
from pathlib import Path
from PIL import Image as IMG
from PIL import ImageSequence
from asyncio import Lock

import imageio
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from typing import Tuple


mutex = Lock()
max_size = 2073600
running = False


async def do_super_resolution(
    image_data: bytes, resize: bool = False, is_gif: bool = False
) -> Tuple[str | BytesIO]:
    """
    对图片进行超分辨率处理
    :param image_data: 图片数据
    :param resize: 是否缩小图片尺寸
    :param is_gif: 是否是gif
    :return: 处理后的图片数据
    """
    global running

    image = IMG.open(BytesIO(image_data))
    image_size = image.size[0] * image.size[1]

    # if len(image_data) >= 4 * (1024 ** 2):
    #     async with mutex:
    #         processing = False
    #     return MessageChain("鉴于QQ对图片文件最大约20M的限制，对图片进行默认超分后预期大小将超过此限制，请尝试缩小图片后再超分")

    upsampler = RealESRGANer(
        scale=4,
        model_path=str(
            Path(__file__).parent.joinpath("RealESRGAN_x4plus_anime_6B.pth")
        ),
        model=RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=6,
            num_grow_ch=32,
            scale=4,
        ),
        tile=100,
        tile_pad=10,
        pre_pad=0,
        half=False,
        gpu_id=0,
    )
    if image_size > max_size:
        # if False:

        if not resize:
            async with mutex:
                running = False
            return f"图片尺寸过大！请发送1080p以内即像素数小于 1920×1080=2073600的照片！\n此图片尺寸为：{image.size[0]}×{image.size[1]}={image_size}！"
        length = 1
        for b in str(max_size / image_size).split(".")[1]:
            if b == "0":
                length += 1
            else:
                break
        magnification = round(max_size / image_size, length + 1)
        image = image.resize(
            (round(image.size[0] * magnification), round(image.size[1] * magnification))
        )
    outputs = []
    output = None
    result = BytesIO()
    if is_gif:
        for i in ImageSequence.Iterator(image):
            image_array: np.ndarray = np.array(i)
            output, _ = upsampler.enhance(image_array, 4)

            outputs.append(output)
    else:
        image_array: np.ndarray = np.array(image)
        # 对图片缩放
        output, _ = upsampler.enhance(image_array, 4)
    if is_gif:
        imageio.mimsave(
            result, outputs, format=".gif", duration=image.info["duration"] / 1000
        )
    else:
        img = IMG.fromarray(output)
        img.save(result, format="PNG")  # format: PNG / JPEG

    async with mutex:
        running = False
    del upsampler

    return result.getvalue()
