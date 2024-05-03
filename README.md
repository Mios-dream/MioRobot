# 澪的简易 QQ 机器人消息处理框架

---

## 概述

编写的一个简单的 QQ 机器人处理消息的框架，可自定义插件
遵循 onebot 标准

## 环境

- python=3.10





## 用法

第一步：

修改 config.json 中的配置信息

第二步：

```bash
pip install -r requirements.txt
```

第三步：

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
	│	└─MessageApi.py	消息发送的模块
	│	
	│	
	└─Event	所有事件处理的模块
		├─EventContral.py 		事件处理中心
		├─GroupMessageEvent.py 	处理群聊事件
		├─PrivateMessageEvent.py	处理私聊事件
		├─NoticeEvent.py 	    处理通知
		├─MetaEvent.py		    处理元事件
		└─RequestEvent.py		处理请求事件

Net	网络处理相关文件
	└─Receives.py	处理websocket请求
```








## 进阶

### 插件编写

所有插件都放在Plugin文件夹中

插件的结构应为

```yaml
Plugin	插件文件夹
	-plugin_1	插件1
		-__init__.py	初始化文件
		-other.py	其他文件
	-plugin_2	插件1
		-__init__.py	初始化文件
		-other.py	其他文件
```



所有的插件都必须包含 __ init __.py





















