# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 添加 Azure Speech SDK DLL 的路径
azure_speech_dll = 'C:\\Users\\xujia\\miniconda3\\envs\\azure-tts\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.core.dll'
if not os.path.exists(azure_speech_dll):
    print(f"Error: {azure_speech_dll} not found. Please update the path.")
    sys.exit(1)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[(azure_speech_dll, '.')],
    datas=collect_data_files('azure.cognitiveservices.speech'),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='text-to-speech-app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['.meta\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='text-to-speech-app',
)
