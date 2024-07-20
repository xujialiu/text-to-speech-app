<p align="center"><img width="100" src="./icon.png" alt="icon" /></p>

<p align="center">Obsidian 文本转音频插件。</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.1-blue" alt="version_tag" />
  <img src="https://img.shields.io/badge/Python-3.10-blue" alt="PyPI - Python Version" >
  <img src="https://img.shields.io/badge/Package-PySide_6-blue"/>
  <img src="https://img.shields.io/badge/Package-Azure-blue"/>


## 文档

[中文文档](./README.zh.md) zht.md) | [英文文档](./README.md)

## 变更日志

[您可以在这里查看最近的变更。](./changelog.md)

## 先决条件

在开始使用此应用之前，您需要事先申请微软的[文本转语音服务](https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/index-text-to-speech)。

## 安装和配置

您可以按照以下步骤配置插件。

### 安装软件

- 请在[此页面](https://github.com/luhaifeng666/obsidian-text2audio/releases)下载最新的软件。

- 按提示安装软件。

- 填写 `Speech key`、`Speech Region` 和 `Directory`。其中，`Speech key`、`Speech Region` 的获取方式可以参考[本文档](https://learn.microsoft.com/zh-cn/azure/ai-services/multi-service-resource?pivots=azportal&tabs=macos#get-the-keys-for-your-resource)。

### 配置应用
- 您可以通过这个[网址](https://portal.azure.com/#home)快速注册或登录**微软Azure云服务**。

- 登录后，点击 `Azure AI services`。
  <p align="left"><img src=".attachments\Pasted_image_20240531141159.png" alt="img" width="800" /></p>
  
- 找到 `Speech service` 后点击 `create`，创建一个服务实例。
  <p align="left"><img src="./.attachments/Pasted_image_20240531141323.png" alt="img" width="800" /></p>
  
- 创建一个 `Resource group`（如果是第一次使用），然后选择离您最近的 `Region`。`Name` 规定全网不能重复，所以请命名长一些，注意：不能有空格或 ` _` 等。`Pricing tier` 选择 `Free F0` 即可。点击 `Review + create`，页面跳转后点击 `Create`。
  <p align="left"><img src="./.attachments/Pasted_image_20240531141619.png" alt="img" width="800" /></p>
  
- 稍等一会儿等待实例创建，点击 `Go to resource`。
  <p align="left"><img src="./.attachments/Pasted_image_20240531142151.png" alt="img" width="800" /></p>
  
- 点击左侧侧边栏的 `Keys and Endpoint`。
  <p align="left"><img src="./.attachments/Pasted_image_20240531142300.png" alt="img" width="800" /></p>
  
- 复制 `KEY` 到 Setting - Basic settings 的 `Speech key`，复制 `Location/Region` 到 `Speech Region`。
  <p align="left"><img src="./.attachments/Pasted_image_20240531142344.png" alt="img" width="800" /></p>
  <p align="left"><img src="./.attachments/Pasted_image_20240531142516.png" alt="img" width="800" /></p>
  
- 选择`Language type`和`Voice type`。如果您觉得语速太慢, 可通过设置`Voice speed`提速。

## 如何使用
该插件有2种使用方式：使用热键和直接使用。

### 使用 Play tab 窗口:

<p align="left"><img src="./.attachments/Snipaste_2024-07-20_17-38-19.png" alt="img" width="800" /></p>

- 点击Start converting: 将开始转换文本框的文字, 并播放到 Speaker。
- 点击Stop Converting: 将停止转换和播放语音。
- 点击Pause / Resume: 用于控制暂停和继续播放。
- 点击Save: 将保存音频文件到选中的文件夹。

### 使用热键

- 设置Setting - Hotkeys
  - Start converting (clipboard text to speech): 触发该热键，将剪切板的文本转换成语音, 并播放到 Speaker。
  - Stop converting and playing: 将停止转换和播放语音。
  - Pause / Resume: 用于控制暂停和继续播放。

