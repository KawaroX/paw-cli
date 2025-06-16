# build_nuitka.py - PAW macOS Application Build Script using Nuitka and delocate
#
# 最终解决方案：这个脚本将使用 Nuitka 进行编译，然后使用专业工具 delocate
# 并为其提供 Homebrew 库路径，以自动修复所有库链接，创建一个完全独立的应用程序。
#
# 如何运行:
# 1. 确保在虚拟环境中已安装 Nuitka 和 delocate: 
#    uv pip install nuitka delocate
# 2. python build_nuitka.py

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
DOWNLOADS_DIR = Path("build_downloads_nuitka")
RESOURCES_DIR = Path("build_resources_nuitka")
PANDOC_EXEC_PATH = RESOURCES_DIR / "pandoc"
# Nuitka 的临时输出目录
NUITKA_OUTPUT_DIR = Path("run_paw.dist")
# 最终的应用目录
FINAL_APP_DIR = Path("dist_paw_nuitka")
# Homebrew 在 Apple Silicon Mac 上的标准库路径
HOMEBREW_LIB_PATH = "/opt/homebrew/lib"


def download_pandoc():
    """下载并解压 Pandoc。"""
    print(">>> 1. Downloading Pandoc for Nuitka build...")
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


def run_nuitka():
    """运行 Nuitka 来编译应用。"""
    print("\n>>> 3. Running Nuitka Compiler...")
    
    command = [
        "python",
        "-m",
        "nuitka",
        "--standalone",
        "--static-libpython=no",
        "--include-package=paw",
        "--include-package-data=certifi",
        "run_paw.py",
    ]
    print(f"Running Nuitka command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Nuitka compilation failed: {e}", file=sys.stderr)
        sys.exit(1)


def fix_bundle_with_delocate():
    """
    (关键修复步骤) 使用 delocate 并为其提供 Homebrew 库路径，以自动修复所有库链接。
    """
    print("\n>>> 4. Fixing bundle with delocate...")
    if not NUITKA_OUTPUT_DIR.is_dir():
        print(f"Error: Nuitka build directory '{NUITKA_OUTPUT_DIR}' not found.", file=sys.stderr)
        return

    python_executable = sys.executable
    command = [
        python_executable,
        "-m",
        "delocate.cmd.delocate_path",
        "--verbose",
        "--lib-path", 
        HOMEBREW_LIB_PATH,
        str(NUITKA_OUTPUT_DIR),
    ]

    try:
        print(f"Running delocate command: {' '.join(command)}")
        subprocess.run(command, check=True)
        print("\n✅ Bundle delocated and fixed successfully.")
    except Exception as e:
        print(f"Delocate failed: {e}", file=sys.stderr)
        sys.exit(1)


def finalize_bundle():
    """将所有内容整合到最终的输出目录。"""
    print("\n>>> 5. Finalizing bundle...")
    # 将 Pandoc 复制到最终的目录
    shutil.copy(PANDOC_EXEC_PATH, NUITKA_OUTPUT_DIR / "pandoc")
    # 将 Nuitka 的输出重命名为我们最终的文件夹名
    if FINAL_APP_DIR.exists():
        shutil.rmtree(FINAL_APP_DIR)
    # 将 Nuitka 生成的 .dist 文件夹重命名为我们的最终目标文件夹
    NUITKA_OUTPUT_DIR.rename(FINAL_APP_DIR)
    # 清理不必要的构建文件夹
    shutil.rmtree("run_paw.build", ignore_errors=True)


if __name__ == "__main__":
    shutil.rmtree(FINAL_APP_DIR, ignore_errors=True)
    shutil.rmtree(NUITKA_OUTPUT_DIR, ignore_errors=True)
    shutil.rmtree("run_paw.build", ignore_errors=True)

    download_pandoc()
    run_nuitka()
    
    if platform.system() == "Darwin":
        fix_bundle_with_delocate()

    finalize_bundle()

    print("\n>>> 6. Build complete!")
    print(f"Your application is ready in the '{FINAL_APP_DIR}' folder.")
    print(f"You can run it via: ./{FINAL_APP_DIR}/run_paw")
