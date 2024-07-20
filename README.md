<p align="center"><img width="100" src="./icon.png" alt="icon" /></p>

<p align="center">Obsidian Text-to-Audio Plugin.</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.1-blue" alt="version_tag" />
  <img src="https://img.shields.io/badge/Python-3.10-blue" alt="PyPI - Python Version" >
  <img src="https://img.shields.io/badge/Package-PySide_6-blue"/>
  <img src="https://img.shields.io/badge/Package-Azure-blue"/>





## Documentation

[Simple Chinese Documentation](./README.zh.md) | [Traditional Chinese Documentation](./README.zht.md) | [English Documentation](./README.md)

## Changelog

[You can view recent changes here.](./changelog.md)

## Prerequisites

Before you start using this plugin, you need to apply for Microsoft's [Text-to-Speech Service](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-text-to-speech) in advance.

## Installation and Configuration

You can configure the plugin by following these steps.

### Installation

- Please download the latest software from [this page](https://github.com/luhaifeng666/obsidian-text2audio/releases).

- Follow the prompts to install the software.

- Fill in the Speech key, Speech Region, and Directory. The acquisition methods for Speech key and Speech Region can be found in [this document](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal&tabs=macos#get-the-keys-for-your-resource).

### Configuration
- You can quickly register or log in to **Microsoft Azure Cloud Services** via this [website](https://portal.azure.com/#home).

- After logging in, click on Azure AI services.
  <p align="left"><img src=".attachments\Pasted_image_20240531141159.png" alt="img" width="800" /></p>
  
- Find the Speech service and click create to create a service instance.
  <p align="left"><img src="./.attachments/Pasted_image_20240531141323.png" alt="img" width="800" /></p>
  
- Create a Resource group (if this is your first time), then select the Region closest to you. Name must be unique across the network, so please name it longer, note: cannot contain spaces or _. Select the Free F0 for Pricing tier. Click Review + create, after the page redirects click Create.
  <p align="left"><img src="./.attachments/Pasted_image_20240531141619.png" alt="img" width="800" /></p>
  
- Wait a while for the instance to be created, then click Go to resource.
  <p align="left"><img src="./.attachments/Pasted_image_20240531142151.png" alt="img" width="800" /></p>
  
- Click on Keys and Endpoint in the left sidebar.
  <p align="left"><img src="./.attachments/Pasted_image_20240531142300.png" alt="img" width="800" /></p>
  
- Copy the KEY to Setting - Basic settings' Speech key, copy Location/Region to Speech Region.
  <p align="left"><img src="./.attachments/Pasted_image_20240531142344.png" alt="img" width="800" /></p>
  <p align="left"><img src="./.attachments/Pasted_image_20240531142516.png" alt="img" width="800" /></p>
  
- Select Language type and Voice type. If you find the speech rate too slow, you can speed up by setting Voice speed.
## How to Use
This plugin can be used in two ways: using hotkeys and directly.

### Using the Play tab window:

<p align="left"><img src="./.attachments/Snipaste_2024-07-20_17-38-19.png" alt="img" width="800" /></p>

- Click Start converting: will begin converting the text in the text box and play it through the Speaker.
- Click Stop Converting: will stop converting and playing the speech.
- Click Pause / Resume: used to control pausing and resuming playback.
- Click Save: will save the audio file to the selected folder.

### Using Hotkeys

- Set Setting - Hotkeys
  - Start converting (clipboard text to speech): Trigger this hotkey to convert text from the clipboard into speech and play it through the Speaker.
  - Stop converting and playing: will stop converting and playing the speech.
  - Pause / Resume: used to control pausing and resuming playback.
