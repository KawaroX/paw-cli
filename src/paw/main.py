import typer
from .commands import new as new_cmd
from .commands import check as check_cmd
from .commands import csl as csl_cmd
from .commands import template as template_cmd
from .commands import add as add_cmd
from .commands import cite as cite_cmd

app = typer.Typer(
    name="paw",
    help="🐾 PAW: A command-line tool for a streamlined Pandoc academic workflow.",
    add_completion=False,
    no_args_is_help=True,
)

# 注册 'new' 和 'check' 命令
app.command(name="new")(new_cmd.new)
app.command(name="check")(check_cmd.check)

# 注册 'add' 命令组
app.add_typer(add_cmd.app, name="add")

# 注册 'cite' 命令
app.command(name="cite")(cite_cmd.cite)

# 注册 'csl' 和 'template' 命令组
app.add_typer(csl_cmd.app, name="csl")
app.add_typer(template_cmd.app, name="template")


if __name__ == "__main__":
    app()
