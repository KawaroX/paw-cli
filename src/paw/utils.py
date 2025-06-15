# 通用工具函数模块

import shutil
import re
from pathlib import Path
import typer
from rich.console import Console
from . import config
from ruamel.yaml import YAML
from pybtex.database import parse_file as parse_bib_file

console = Console()
yaml = YAML()
yaml.preserve_quotes = True
# 设置 YAML 缩进，使其更美观
yaml.indent(mapping=2, sequence=4, offset=2)


def ensure_paw_dirs():
    """确保 PAW 全局资源目录存在"""
    try:
        config.PAW_HOME_DIR.mkdir(exist_ok=True)
        config.CSL_DIR.mkdir(exist_ok=True)
        config.TEMPLATES_DIR.mkdir(exist_ok=True)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold] Could not create PAW home directories in '{config.PAW_HOME_DIR}'.")
        console.print(f"Reason: {e}")
        raise typer.Exit(1)


def find_project_root() -> Path | None:
    """通过寻找 .paw-project 标记文件（或 Makefile）来确定项目根目录"""
    current_dir = Path.cwd().resolve()
    for _ in range(8): # 最多向上查找8级
        # 优先寻找 Makefile
        if (current_dir / "Makefile").exists() and (current_dir / "manuscript").is_dir():
            return current_dir
        if current_dir.parent == current_dir: # 到达根目录
            break
        current_dir = current_dir.parent
    return None


def get_project_paths():
    """获取当前 PAW 项目的关键路径"""
    root = find_project_root()
    if not root:
        console.print("[bold red]Error:[/bold] Not inside a PAW project. Could not find project root.")
        raise typer.Exit(1)
    
    paths = {
        "root": root,
        "manuscript": root / "manuscript",
        "resources": root / "resources",
        "figures": root / "figures",
        "frontmatter": root / "manuscript" / "00-frontmatter.md"
    }

    if not paths["frontmatter"].exists():
        console.print(f"[bold red]Error:[/bold] Frontmatter file not found at '{paths['frontmatter']}'")
        raise typer.Exit(1)

    return paths


def update_yaml_list(yaml_path: Path, key: str, value: str):
    """
    智能地更新 YAML 文件中的一个键。
    如果该键的值是字符串,则将其转换为列表。
    如果已经是列表,则向列表中添加新值。
    """
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            docs = list(yaml.load_all(f))
        
        if not docs:
            raise ValueError("YAML file is empty or invalid.")

        frontmatter = docs[0]
        
        if key not in frontmatter:
            frontmatter[key] = [value]
        else:
            current_value = frontmatter[key]
            if isinstance(current_value, str):
                # 如果当前值是字符串且与新值不同,则转换为列表
                if current_value != value:
                    frontmatter[key] = [current_value, value]
                # 如果相同,则什么都不做
            elif isinstance(current_value, list):
                # 如果已经是列表,且新值不在其中,则添加
                if value not in current_value:
                    current_value.append(value)
            else:
                # 处理其他可能的类型,简单起见直接覆盖为列表
                 frontmatter[key] = [value]

        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump_all(docs, f)

        console.print(f"[green]✓ Updated '{key}' in '{yaml_path.name}'.[/green]")

    except Exception as e:
        console.print(f"[bold red]Error updating YAML file: {e}[/bold red]")
        raise typer.Exit(1)


class ResourceHandler:
    """处理 CSL 和 Template 资源的通用逻辑类"""
    def __init__(self, resource_type: str, resource_ext: str, global_dir: Path, yaml_key: str):
        self.resource_type = resource_type
        self.resource_ext = resource_ext
        self.global_dir = global_dir
        self.yaml_key = yaml_key
        ensure_paw_dirs()

    def add(self, source_path: Path):
        if not source_path.exists():
            console.print(f"[bold red]Error:[/bold] File not found at '{source_path}'")
            raise typer.Exit(1)

        if source_path.suffix != self.resource_ext:
            console.print(f"[bold red]Error:[/bold] File must be a '{self.resource_ext}' file.")
            raise typer.Exit(1)

        dest_path = self.global_dir / source_path.name
        try:
            shutil.copy(source_path, dest_path)
            console.print(f"[green]Successfully added '{source_path.name}' to the global {self.resource_type} library.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error adding {self.resource_type}: {e}[/bold red]")
            raise typer.Exit(1)

    def remove(self, name: str):
        if not name.endswith(self.resource_ext):
            name += self.resource_ext
        
        target_path = self.global_dir / name
        if not target_path.exists():
            console.print(f"[bold red]Error:[/bold] {self.resource_type.capitalize()} '{name}' not found in the global library.")
            raise typer.Exit(1)

        try:
            target_path.unlink()
            console.print(f"[green]Successfully removed '{name}' from the global {self.resource_type} library.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error removing {self.resource_type}: {e}[/bold red]")
            raise typer.Exit(1)

    def list_items(self):
        console.print(f"Available global {self.resource_type}s in [cyan]{self.global_dir}[/cyan]:")
        items = sorted([f.name for f in self.global_dir.glob(f"*{self.resource_ext}")])
        if not items:
            console.print(f"  No {self.resource_type}s found.")
            return

        for item in items:
            console.print(f"- {item}")
    
    def use(self, name: str):
        if not name.endswith(self.resource_ext):
            name += self.resource_ext

        source_path = self.global_dir / name
        if not source_path.exists():
            console.print(f"[bold red]Error:[/bold] {self.resource_type.capitalize()} '{name}' not found in the global library.")
            raise typer.Exit(1)

        project_paths = get_project_paths()
        dest_path = project_paths["resources"] / name

        # 复制文件
        try:
            shutil.copy(source_path, dest_path)
            console.print(f"[green]✓ Copied '{name}' to '{dest_path}'.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error copying file: {e}[/bold red]")
            raise typer.Exit(1)

        # 更新 YAML frontmatter
        try:
            with open(project_paths["frontmatter"], 'r', encoding='utf-8') as f:
                docs = list(yaml.load_all(f))
            
            if not docs:
                raise ValueError("Frontmatter file is empty.")

            frontmatter = docs[0]
            frontmatter[self.yaml_key] = name

            with open(project_paths["frontmatter"], 'w', encoding='utf-8') as f:
                yaml.dump_all(docs, f)

            console.print(f"[green]✓ Updated '{self.yaml_key}' in '{project_paths['frontmatter'].name}'.[/green]")

        except Exception as e:
            console.print(f"[bold red]Error updating YAML frontmatter: {e}[/bold red]")
            raise typer.Exit(1)
