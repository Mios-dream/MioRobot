# 澪的简易 QQ 机器人消息处理框架

---

<div align="center">

![MioRobot](https://counter.seku.su/cmoe?name=miosdream&theme=r34)

![os](https://img.shields.io/badge/os-win,linux,mac-orange?style=for-the-badge) ![python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge) [![License](https://img.shields.io/badge/LICENSE-GPL_3.0-green.svg?style=for-the-badge)](./LICENSE)

</div>

<style>
.light{
    font-size: 50px;
    color: #FFC0CB;
    text-shadow: 0 0 0.5em #FFC0CB, 0 0 0.2em #FFC0CB;
} 
</style>
<div class="light" align="center"><font face="楷体">“我愿用我最真挚的感情打动你的心灵”</font></div>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<style type="text/css">
            .neon {
        color: #cce7f8;
        font-size: 2.5rem;
        -webkit-animation: shining 0.5s alternate infinite;
        animation: shining 0.5s alternate infinite;
    }
    @-webkit-keyframes shining {
        from {
            text-shadow: 0 0 10px lightblue, 0 0 20px lightblue, 0 0 30px lightblue, 0 0 40px skyblue, 0 0 50px skyblue, 0 0 60px skyblue;
        }

<table style="display: table; border-collapse: collapse; margin: auto; background-color:transparent;">
<tbody><tr>
<td style="vertical-align: top; color:#B2B7F2; font-size:36px; font-family:'Times New Roman',serif; font-weight:bold; text-align:left; padding:10px 10px; line-height:100%">“</td>
    <td style="text-align: center; padding: 1em; vertical-align: middle;"><font face="楷体"><span style="color:#FFC0CB;"><b>请阁下一直喜欢澪哦！</b></span></font></td>
<td style="vertical-align: bottom; color:#B2B7F2; font-size:36px; font-family:'Times New Roman',serif; font-weight:bold; text-align:left; padding:10px 10px; line-height:100%">”</td>
</tr>
</tbody></table>

## 概述

一个简单的 QQ 机器人处理消息的框架，可自定义插件遵循 onebot 标准

## 环境

- python=3.10

## 用法

(可选)建议使用 conda 创建虚拟环境运行

```shell
conda create -n mio_robot python=3.10
```

```shell
conda activate mio_robot
```

#### 第一步：

修改 config.json 中的配置信息

#### 第二步：

```bash
pip install -r requirements.txt
```

#### 第三步：

```bash
python main.py
```

## 目录结构

```dir
DataType	数据类型文件夹
   ├─CQcode.py	CQ码的解析
   ├─MessageData.py 	消息类型基类
   ├─GroupMassageData.py	群消息数据类型
   └─PrivateMessageDate.py 	私聊消息数据类型

Plugin	插件文件夹
   ├─plugin_1
   └─plugin_2

Models	必要模块
   ├─Api	所有消息发送api模块
   │   └─MessageApi.py	消息发送的模块
   │
   └─Event	所有事件处理的模块
      ├─EventContral.py		事件处理中心
      ├─GroupMessageEvent.py 	处理群聊事件
      ├─PrivateMessageEvent.py	处理私聊事件
      ├─NoticeEvent.py 	    处理通知
      ├─MetaEvent.py	处理元事件
      └─RequestEvent.py		处理请求事件

Net	网络处理相关文件
   └─Receives.py	处理websocket请求
```

## 进阶

- [1.插件编写](./src/md/plugin.md)

## 其他

- [1.澪的介绍](./src/md/mio.md)

## 特别鸣谢

<div align="center">
    <h3>
--------------------感谢一路以来陪着我的朋友们---------------------
    </h3>
</div>

<a href="https://github.com/Mios-dream/MioRobot/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=Mios-dream/MioRobot" />
</a>
