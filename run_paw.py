# run_paw.py - PyInstaller Entry Point
#
# 这个脚本是专门为 PyInstaller 打包准备的入口点。
# 它解决了在 src-layout 结构中遇到的相对导入问题，
# 并加入了关键的 sudo 权限检查，从根源上防止权限错误。

import os
import sys

def main():
    """
    应用程序的主入口函数。
    """
    # ----------------------------------------------------------------------
    # 最终解决方案：Sudo 权限检查
    # 在导入任何我们自己的代码之前，首先检查权限。
    # os.geteuid() == 0 表示当前用户是 root。
    # ----------------------------------------------------------------------
    try:
        if os.geteuid() == 0:
            print("\033[91mError: Do not run PAW with sudo or as the root user.\033[0m", file=sys.stderr)
            print("Running as root will create project files with incorrect permissions,", file=sys.stderr)
            print("leading to 'Permission Denied' errors in the future.", file=sys.stderr)
            print("Please run PAW as a regular user.", file=sys.stderr)
            sys.exit(1)
    except AttributeError:
        # os.geteuid() 在非 Unix-like 系统（如 Windows）上不存在，
        # 我们可以安全地忽略这个检查。
        pass

    # 只有在权限检查通过后，才导入并运行我们的主应用
    from paw.main import app
    sys.exit(app())


if __name__ == "__main__":
    main()

