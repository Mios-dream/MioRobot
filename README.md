# 澪的简易 QQ 机器人消息处理框架

---

<div align="center">

[![QQGroup](https://img.shields.io/badge/点击加入我们-%E2%9D%A4-red?style=for-the-badge&labelColor=orange)](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=FgoIQ8GMNUtKrM8BytEMNV6iEbCUj06j&authKey=Z%2Bnd%2BhPQ5BTllW%2BZ13HBYnbmC81HD7XG9DZyXoEgcy55D4N6em%2B0zDC2Hsxjp3s9&noverify=0&group_code=676832751)

![MioRobot](https://counter.seku.su/cmoe?name=miosdream&theme=r34)

![os](https://img.shields.io/badge/os-win,linux,mac-orange?style=for-the-badge) ![python](https://img.shields.io/badge/python-3.7+-blue?style=for-the-badge) [![License](https://img.shields.io/badge/LICENSE-GPL_3.0-green.svg?style=for-the-badge)](./LICENSE)

</div>

<br>


<div align="center">
<img src="src/md/assets/text.png" decoding="async" loading="lazy" width="1080" height="">
<table style="display: table; border-collapse: collapse; margin: auto; background-color:transparent;">
<tbody><tr>
<td style="vertical-align: top; color:#B2B7F2; font-size:36px; font-family:'Times New Roman',serif; font-weight:bold; text-align:left; padding:10px 10px; line-height:100%">“</td>
    <td style="text-align: center; padding: 1em; vertical-align: middle;"><font face="楷体"><span style="color:#FFC0CB;"><b>请阁下一直喜欢澪哦！</b></span></font></td>
<td style="vertical-align: bottom; color:#B2B7F2; font-size:36px; font-family:'Times New Roman',serif; font-weight:bold; text-align:left; padding:10px 10px; line-height:100%">”</td>
</tr>
</tbody></table>
</div>

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

log.py	日志类
plugins.py	插件基类
plugin_loader.py	插件加载器
const.py	常量类
init_config.py	初始化设置类
main.py	主程序
```

## 进阶

- [1.插件编写](./src/md/plugin.md)

## 其他

- [1.澪的介绍](./src/md/mio.md)
- [2.插件列表](./src/md/plugin_list.md)

## 特别鸣谢

<div align="center">
    <h3>
--------------------感谢一路以来陪着我的朋友们---------------------
    </h3>
</div>

<a href="https://github.com/Mios-dream/MioRobot/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=Mios-dream/MioRobot" />
</a>
