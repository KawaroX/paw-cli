# build_app.py - PAW macOS Application Build Script
#
# 最终解决方案：这个脚本将使用最直接和可靠的方式，自动查找 pyenv 环境的
# Python 共享库，并使用 --add-binary 和 --paths 参数强制打包，以构建一个
# 完全独立的、能正确找到其源代码的应用程序。
#
# 如何运行:
# python build_app.py

import os
import sys
import platform
import requests
import shutil
import subprocess
import zipfile
from pathlib import Path

# --- 配置 ---
PANDOC_VERSION = "3.7.0.2"
PANDOC_MACOS_URL = f"https://github.com/jgm/pandoc/releases/download/{PANDOC_VERSION}/pandoc-{PANDOC_VERSION}-arm64-macOS.zip"
DOWNLOADS_DIR = Path("build_downloads")
RESOURCES_DIR = Path("build_resources")
PANDOC_EXEC_PATH = RESOURCES_DIR / "pandoc"


def download_pandoc():
    """下载并解压 Pandoc。"""
    print(">>> 1. Downloading Pandoc...")
    if PANDOC_EXEC_PATH.exists():
        print("Pandoc already exists. Skipping download.")
        return

    DOWNLOADS_DIR.mkdir(exist_ok=True)
    RESOURCES_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / "pandoc.zip"

    try:
        print(f"Downloading from {PANDOC_MACOS_URL}...")
        with requests.get(PANDOC_MACOS_URL, stream=True) as r:
            r.raise_for_status()
            with open(archive_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded Pandoc archive to {archive_path}")

        print(">>> 2. Extracting Pandoc...")
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            pandoc_member_path = None
            for member in zip_ref.infolist():
                if member.filename.endswith("bin/pandoc") and not member.is_dir():
                    pandoc_member_path = member.filename
                    break
            if not pandoc_member_path:
                raise FileNotFoundError("Could not find 'bin/pandoc' in the downloaded archive.")

            with zip_ref.open(pandoc_member_path) as source_file:
                with open(PANDOC_EXEC_PATH, 'wb') as target_file:
                    shutil.copyfileobj(source_file, target_file)

        print(f"Extracted Pandoc executable to {PANDOC_EXEC_PATH}")
        PANDOC_EXEC_PATH.chmod(0o755)

    except Exception as e:
        print(f"Error during Pandoc setup: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if archive_path.exists():
            archive_path.unlink()
        if DOWNLOADS_DIR.exists():
            try:
                DOWNLOADS_DIR.rmdir()
            except OSError:
                pass


def find_pyenv_python_lib():
    """
    使用 shell 命令精确查找当前 pyenv 环境的 dylib 路径。
    """
    print(">>> 3. Finding pyenv Python shared library...")
    try:
        # 首先获取 pyenv 的根目录
        prefix_result = subprocess.run(["pyenv", "prefix"], check=True, capture_output=True, text=True)
        pyenv_prefix = prefix_result.stdout.strip()
        
        # 在该目录下查找 dylib
        find_command = f'find "{pyenv_prefix}/lib" -name "libpython*.dylib"'
        lib_result = subprocess.run(find_command, shell=True, check=True, capture_output=True, text=True)
        lib_path = lib_result.stdout.strip().splitlines()[0] # 取第一个结果
        
        if not lib_path or not Path(lib_path).exists():
             raise FileNotFoundError
        return lib_path
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        print("Error: Could not automatically find the Python shared library in your pyenv environment.", file=sys.stderr)
        print("Please ensure 'pyenv' is correctly installed and configured.", file=sys.stderr)
        sys.exit(1)


def run_final_build():
    """运行最终的、最可靠的构建流程。"""
    python_lib_path = find_pyenv_python_lib()
    print(f"Found Python shared library at: {python_lib_path}")

    # 构建 PyInstaller 命令
    command = [
        "python", # 使用当前虚拟环境的 python
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean", # 每次都进行清理
        "--name", "paw",
        # 关键修复：告诉 PyInstaller 我们的源代码在哪里！
        "--paths", "src",
        "--add-data", f"{PANDOC_EXEC_PATH.resolve()}:.",
        # 关键步骤：显式添加找到的 dylib
        "--add-binary", f"{python_lib_path}:.",
        # 添加一些常见的、PyInstaller 容易遗漏的隐藏依赖
        "--hidden-import", "pkg_resources.py2_warn",
        "--hidden-import", "requests",
        "--hidden-import", "pybtex",
        "--hidden-import", "pyperclip",
        "--hidden-import", "rich",
        "--hidden-import", "ruamel.yaml",
        "run_paw.py",
    ]
    
    print("\n>>> 4. Running PyInstaller with final configuration...")
    print(f"Command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Final build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    download_pandoc()
    run_final_build()

    print("\n>>> 5. Build complete!")
    print(f"Your application is ready in the 'dist' folder.")
    print(f"You can run it via: ./dist/paw")
