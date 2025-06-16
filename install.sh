#!/bin/bash
#
# PAW CLI Installer Script for macOS & Linux
# ==========================================
#
# 这个脚本会自动从 GitHub Releases 下载最新预编译的 PAW 二进制文件，
# 并将其安装到 /usr/local/bin，从而让用户可以在任何位置直接使用 `paw` 命令。
#
# 用户使用方法:
# curl -sSL https://raw.githubusercontent.com/your-username/paw-cli/main/install.sh | sudo bash

# --- 配置 (请修改为你自己的仓库信息) ---
GITHUB_REPO="KawaroX/paw-cli
INSTALL_DIR="/usr/local/bin"
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
    echo_color "1;31" "请像这样运行: curl -sSL ... | sudo bash"
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
elif [ "$OS" == "Linux" ]; then
     if [ "$ARCH" == "x86_64" ]; then
        TARGET_OS="linux-amd64"
     else
        echo_color "1;31" "错误：不支持的 Linux 架构: $ARCH"
        exit 1
     fi
else
    echo_color "1;31" "错误：不支持的操作系统: $OS"
    exit 1
fi

echo_color "1;32" ">>> 检测到你的系统是: $OS ($ARCH)"

# 3. 通过 GitHub API 查找最新的发布版本
echo_color "1;32" ">>> 正在查找最新的 PAW CLI 版本..."
LATEST_RELEASE_URL="https://api.github.com/repos/${GITHUB_REPO}/releases/latest"
LATEST_VERSION=$(curl -sSL "$LATEST_RELEASE_URL" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_VERSION" ]; then
    echo_color "1;31" "错误：无法从 GitHub 找到最新的发布版本。"
    exit 1
fi

echo_color "1;32" "最新的版本是: $LATEST_VERSION"

# 4. 构建下载链接并下载
ASSET_NAME="${EXE_NAME}-${LATEST_VERSION}-${TARGET_OS}.tar.gz"
DOWNLOAD_URL="https://github.com/${GITHUB_REPO}/releases/download/${LATEST_VERSION}/${ASSET_NAME}"
TMP_DIR=$(mktemp -d)
TMP_ARCHIVE="$TMP_DIR/$ASSET_NAME"

echo_color "1;32" ">>> 正在下载 PAW CLI (这可能需要一些时间)..."
echo "下载地址: $DOWNLOAD_URL"

# 关键修复：移除 -s (静默) 参数，使用 --progress-bar 来显示进度条
curl --progress-bar -L -o "$TMP_ARCHIVE" "$DOWNLOAD_URL"
if [ $? -ne 0 ]; then
    echo_color "1;31" "\n错误：下载发布文件失败。"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 5. 解压压缩包
echo_color "1;32" ">>> 正在解压..."
tar -xzf "$TMP_ARCHIVE" -C "$TMP_DIR"
if [ $? -ne 0 ]; then
    echo_color "1;31" "错误：解压失败。"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 6. 安装可执行文件
EXTRACTED_EXE=$(find "$TMP_DIR" -type f -name "$EXE_NAME" | head -n 1)
if [ -z "$EXTRACTED_EXE" ]; then
    echo_color "1;31" "错误：在压缩包中找不到名为 '$EXE_NAME' 的可执行文件。"
    rm -rf "$TMP_DIR"
    exit 1
fi

TARGET_EXE="$INSTALL_DIR/$EXE_NAME"
echo_color "1;32" ">>> 正在安装 PAW CLI 到 $TARGET_EXE..."
mv "$EXTRACTED_EXE" "$TARGET_EXE"
if [ $? -ne 0 ]; then
    echo_color "1;31" "错误：移动文件失败，请检查 $INSTALL_DIR 的写入权限。"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 7. 设置执行权限并清理
chmod +x "$TARGET_EXE"
rm -rf "$TMP_DIR"

echo_color "1;32" "\n✅ PAW CLI 已成功安装！"
echo_color "1;32" "现在你可以在终端的任何位置运行 '$EXE_NAME --help'。"
