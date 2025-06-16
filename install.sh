#!/bin/bash
#
# PAW CLI Installer Script for macOS & Linux
# ==========================================
#
# (最终版) 这个脚本会自动下载并正确安装 PAW CLI，
# 将整个应用包放置在 /usr/local/opt，并创建一个符号链接到 /usr/local/bin。
#
# 用户使用方法:
# curl -sSL https://raw.githubusercontent.com/KawaroX/paw-cli/main/install.sh | sudo -E bash

# --- 配置 ---
GITHUB_REPO="KawaroX/paw-cli"
# 将整个应用安装到这个目录
APP_INSTALL_DIR="/usr/local/opt/paw-cli"
# 在这个目录创建符号链接
BIN_DIR="/usr/local/bin"
EXE_NAME="paw"
# --- 配置结束 ---

# 带有颜色的输出函数
echo_color() {
    local color_code=$1
    shift
    echo -e "\033[${color_code}m$@\033[0m"
}

# 1. 检查 root 权限
if [ "$(id -u)" -ne 0 ]; then
    echo_color "1;31" "错误：此脚本需要使用 sudo 运行。"
    echo_color "1;31" "请像这样运行: curl ... | sudo -E bash"
    exit 1
fi

# 2. 检测操作系统和架构
OS=$(uname -s)
ARCH=$(uname -m)

if [ "$OS" == "Darwin" ]; then
    if [ "$ARCH" == "arm64" ]; then
        TARGET_OS="macos-arm64"
    else
        TARGET_OS="macos-x86_64"
    fi
else
    echo_color "1;31" "错误：仅支持 macOS。"
    exit 1
fi

echo_color "1;32" ">>> 检测到你的系统是: $OS ($ARCH)"

# 3. 查找最新的发布版本
echo_color "1;32" ">>> 正在查找最新的 PAW CLI 版本..."
LATEST_RELEASE_URL="https://api.github.com/repos/${GITHUB_REPO}/releases/latest"
LATEST_VERSION=$(curl -sSL "$LATEST_RELEASE_URL" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_VERSION" ]; then
    echo_color "1;31" "错误：无法从 GitHub 找到最新的发布版本。"
    exit 1
fi

echo_color "1;32" "最新的版本是: $LATEST_VERSION"

# 4. 下载并解压
ASSET_NAME="paw-${LATEST_VERSION}-${TARGET_OS}.tar.gz"
DOWNLOAD_URL="https://github.com/${GITHUB_REPO}/releases/download/${LATEST_VERSION}/${ASSET_NAME}"
TMP_DIR=$(mktemp -d)
TMP_ARCHIVE="$TMP_DIR/$ASSET_NAME"

echo_color "1;32" ">>> 正在下载 PAW CLI..."
echo "下载地址: $DOWNLOAD_URL"
curl -fL -# -o "$TMP_ARCHIVE" "$DOWNLOAD_URL"
if [ $? -ne 0 ]; then
    echo_color "1;31" "\n错误: 下载失败。请检查你的网络连接。"
    rm -rf "$TMP_DIR"
    exit 1
fi

echo_color "1;32" ">>> 正在解压..."
tar -xzf "$TMP_ARCHIVE" -C "$TMP_DIR"
# 解压后，我们应该得到一个名为 `paw` 的文件夹
EXTRACTED_APP_DIR="$TMP_DIR/paw"
if [ ! -d "$EXTRACTED_APP_DIR" ]; then
    echo_color "1;31" "错误：压缩包中没有找到 'paw' 文件夹。"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 5. 安装整个应用文件夹
echo_color "1;32" ">>> 正在安装 PAW CLI 到 $APP_INSTALL_DIR..."
# 在安装前先删除可能存在的旧版本
rm -rf "$APP_INSTALL_DIR"
# 创建父目录 (如果不存在)
mkdir -p "$(dirname "$APP_INSTALL_DIR")"
# 移动整个文件夹
mv "$EXTRACTED_APP_DIR" "$APP_INSTALL_DIR"

# 6. 创建符号链接
TARGET_LINK="$BIN_DIR/$EXE_NAME"
REAL_EXE_PATH="$APP_INSTALL_DIR/$EXE_NAME"
echo_color "1;32" ">>> 正在创建符号链接到 $TARGET_LINK..."
# -f 强制覆盖已存在的链接, -s 创建符号链接
ln -sf "$REAL_EXE_PATH" "$TARGET_LINK"

# 7. 清理
rm -rf "$TMP_DIR"

echo_color "1;32" "\n✅ PAW CLI 已成功安装！"
echo_color "1;32" "现在你可以在终端的任何位置运行 '$EXE_NAME --help'。"
