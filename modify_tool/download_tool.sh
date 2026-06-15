#!/usr/bin/env bash
set -euo pipefail

OS="$(uname -s)"

if [[ "$OS" == "Linux" ]]; then
    echo "Detected Linux, downloading with wget..."
    wget -O X-Anylabeling-Linux-CPU https://yubinux.cn/tmp/X-Anylabeling-Linux-CPU
elif [[ "$OS" == "MINGW"* || "$OS" == "MSYS"* || "$OS" == "CYGWIN"* ]]; then
    echo "Detected Windows, downloading with PowerShell..."
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/CVHub520/X-AnyLabeling/releases/download/v3.3.10/X-AnyLabeling-CPU.exe' -OutFile 'X-AnyLabeling-CPU.exe'"
else
    echo "Unsupported OS: $OS"
    exit 1
fi