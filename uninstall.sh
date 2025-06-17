#!/bin/bash
#
# PAW CLI Uninstaller Script for macOS & Linux
# ============================================
#
# 这个脚本会安全、完整地从你的系统中移除 PAW CLI 及其所有相关文件。

# --- 配置 ---
APP_INSTALL_DIR="/usr/local/opt/paw-cli"
BIN_LINK="/usr/local/bin/paw"
USER_DATA_DIR="$HOME/.paw"
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
    exit 1
fi

echo_color "1;33" "PAW CLI Uninstaller"
echo "--------------------------"

# 2. 移除符号链接
if [ -L "$BIN_LINK" ]; then
    echo_color "1;32" ">>> 正在移除命令: $BIN_LINK..."
    rm -f "$BIN_LINK"
    if [ $? -eq 0 ]; then
        echo "✅  成功移除。"
    else
        echo_color "1;31" "错误：移除符号链接失败。"
    fi
else
    echo_color "0;37" "命令链接不存在，跳过。"
fi

# 3. 移除主程序文件夹
if [ -d "$APP_INSTALL_DIR" ]; then
    echo_color "1;32" "\n>>> 正在移除主程序: $APP_INSTALL_DIR..."
    rm -rf "$APP_INSTALL_DIR"
    if [ $? -eq 0 ]; then
        echo "✅  成功移除。"
    else
        echo_color "1;31" "错误：移除主程序文件夹失败。"
    fi
else
    echo_color "0;37" "主程序文件夹不存在，跳过。"
fi

# 4. (关键步骤) 询问用户是否要移除数据
if [ -d "$USER_DATA_DIR" ]; then
    echo_color "1;33" "\n>>> 检测到用户数据文件夹: $USER_DATA_DIR"
    echo "这个文件夹包含了你使用 'paw csl add' 和 'paw template add' 添加的所有全局样式和模板。"
    
    # 切换回原始用户来执行 `read` 命令，避免 `sudo` 环境的干扰
    # `who am i | awk '{print $1}'` 或 `logname` 可以获取当前登录的用户名
    SUDO_USER=$(logname)
    su - "$SUDO_USER" -c "read -p '你想要移除这个文件夹吗？其中的数据将永久丢失！[y/N]: ' -r "
    
    # 获取用户的输入
    REPLY=$(su - "$SUDO_USER" -c 'echo $REPLY')

    if [[ "$REPLY" =~ ^[Yy]$ ]]; then
        echo_color "1;32" ">>> 正在移除用户数据文件夹..."
        rm -rf "$USER_DATA_DIR"
        echo "✅  成功移除。"
    else
        echo_color "0;37" "已保留用户数据文件夹。"
    fi
else
    echo_color "0;37" "\n未找到用户数据文件夹，无需处理。"
fi

echo_color "1;32" "\n卸载完成！感谢你使用 PAW。🐾"
