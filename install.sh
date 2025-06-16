#!/bin/bash
#
# PAW CLI Installer Script for macOS & Linux (with proxy support)
# ==========================================
#
# 用户使用方法:
# curl -sSL https://raw.githubusercontent.com/KawaroX/paw-cli/main/install.sh | sudo bash

# --- 配置 ---
GITHUB_REPO="KawaroX/paw-cli"
INSTALL_DIR="/usr/local/bin"
EXE_NAME="paw"
# --- 配置结束 ---

# 带有颜色的输出函数
echo_color() {
    local color_code=$1
    shift
    echo -e "\033[${color_code}m$@\033[0m"
}

# 检查 root 权限
if [ "$(id -u)" -ne 0 ]; then
    echo_color "1;31" "错误：此脚本需要使用 sudo 运行。"
    echo_color "1;31" "请像这样运行: curl -sSL ... | sudo bash"
    exit 1
fi

# 检测操作系统和架构
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

# 检查代理环境变量
if [ -n "$https_proxy" ] || [ -n "$HTTPS_PROXY" ] || [ -n "$ALL_PROXY" ] || [ -n "$all_proxy" ]; then
    echo_color "1;34" "检测到代理环境变量，curl/wget 将自动使用代理。"
else
    echo_color "1;33" "未检测到代理环境变量。如果你在中国大陆，建议设置代理以加速 GitHub 下载。"
    echo_color "1;33" "例如：export https_proxy=\"http://127.0.0.1:7890\""
fi

# 通过 GitHub API 查找最新的发布版本
echo_color "1;32" ">>> 正在查找最新的 PAW CLI 版本..."
LATEST_RELEASE_URL="https://api.github.com/repos/${GITHUB_REPO}/releases/latest"
LATEST_VERSION=$(curl -sSL "$LATEST_RELEASE_URL" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_VERSION" ]; then
    echo_color "1;31" "错误：无法从 GitHub 找到最新的发布版本。"
    exit 1
fi

echo_color "1;32" "最新的版本是: $LATEST_VERSION"

# 构建下载链接并下载
ASSET_NAME="${EXE_NAME}-${LATEST_VERSION}-${TARGET_OS}.tar.gz"
DOWNLOAD_URL="https://github.com/${GITHUB_REPO}/releases/download/${LATEST_VERSION}/${ASSET_NAME}"
TMP_DIR=$(mktemp -d)
TMP_ARCHIVE="$TMP_DIR/$ASSET_NAME"

echo_color "1;32" ">>> 正在下载 PAW CLI (这可能需要一些时间)..."
echo "下载地址: $DOWNLOAD_URL"

# 下载函数，支持 curl/wget，自动使用代理
download_with_retry() {
    local url="$1"
    local output="$2"
    local try=1
    local max_try=3
    while [ $try -le $max_try ]; do
        if command -v curl >/dev/null 2>&1; then
            curl -fL --http1.1 --connect-timeout 20 --retry 2 -o "$output" "$url"
            CURL_EXIT_CODE=$?
            if [ $CURL_EXIT_CODE -eq 0 ]; then
                return 0
            fi
        elif command -v wget >/dev/null 2>&1; then
            wget -q -O "$output" --timeout=20 --tries=2 "$url"
            WGET_EXIT_CODE=$?
            if [ $WGET_EXIT_CODE -eq 0 ]; then
                return 0
            fi
        else
            echo_color "1;31" "错误: 下载失败，你的系统需要安装 curl 或 wget。"
            return 1
        fi
        echo_color "1;33" "第 $try 次下载失败，正在重试..."
        try=$((try+1))
        sleep 2
    done
    return 1
}

download_with_retry "$DOWNLOAD_URL" "$TMP_ARCHIVE"
if [ $? -ne 0 ]; then
    echo_color "1;31" "\n❌ 错误: 无法下载文件。"
    echo_color "1;33" "常见原因："
    echo_color "1;33" "1. 你的网络环境无法直连 GitHub Releases（被墙或限速）"
    echo_color "1;33" "2. 没有配置代理"
    echo_color "1;33" "3. DNS 污染或 SSL 被干扰"
    echo_color "1;33" "解决办法："
    echo_color "1;33" "1. 配置代理后重新运行本脚本，例如："
    echo_color "1;36" "   export https_proxy=\"http://127.0.0.1:7890\""
    echo_color "1;33" "2. 或者用浏览器手动下载："
    echo_color "1;36" "   $DOWNLOAD_URL"
    echo_color "1;33" "   然后解压并将 paw 移动到 /usr/local/bin"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 解压压缩包
echo_color "1;32" ">>> 正在解压..."
tar -xzf "$TMP_ARCHIVE" -C "$TMP_DIR"
if [ $? -ne 0 ]; then
    echo_color "1;31" "错误：解压失败。"
    rm -rf "$TMP_DIR"
    exit 1
fi

# 安装可执行文件
EXTRACTED_EXE=$(find "$TMP_DIR" -type f -name "$EXE_NAME" | head -n 1)
if [ -z "$EXTRACTED_EXE" ]; then
    EXTRACTED_EXE=$(find "$TMP_DIR" -type f -name "${EXE_NAME}.bin" | head -n 1)
fi

if [ -z "$EXTRACTED_EXE" ]; then
    echo_color "1;31" "错误：在压缩包中找不到名为 '$EXE_NAME' 的可执行文件。"
    rm -rf "$TMP_DIR"
    exit 1
fi

TARGET_EXE="$INSTALL_DIR/$EXE_NAME"
echo_color "1;32" ">>> 正在安装 PAW CLI 到 $TARGET_EXE..."
rm -f "$TARGET_EXE"
mv "$EXTRACTED_EXE" "$TARGET_EXE"
if [ $? -ne 0 ]; then
    echo_color "1;31" "错误：移动文件失败，请检查 $INSTALL_DIR 的写入权限。"
    rm -rf "$TMP_DIR"
    exit 1
fi

chmod +x "$TARGET_EXE"
rm -rf "$TMP_DIR"

echo_color "1;32" "\n✅ PAW CLI 已成功安装！"
echo_color "1;32" "现在你可以在终端的任何位置运行 '$EXE_NAME --help'。"
