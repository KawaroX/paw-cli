# 包含所有项目模板文件内容的模块

import textwrap

def get_frontmatter_template(title: str) -> str:
    # 使用 textwrap.dedent 来移除代码中因对齐产生的多余空格
    # 注意: 所有 Pandoc 语法中的 `{}` 都需要写成 `{{` 和 `}}` 来进行转义,
    # 从而避免与 Python 的 f-string 语法冲突。
    return textwrap.dedent(f'''
        ---
        # ----------------------------------------------------------------------
        # 文档元数据 (YAML Frontmatter)
        # ----------------------------------------------------------------------
        # 更多Pandoc元数据变量, 请参考: https://pandoc.org/MANUAL.html#variables

        # -- 核心元数据 --
        title: "{title}"
        author:
          - 你的名字
        date: today # `today` 会自动替换为当前日期
        abstract: |
          这里是你的摘要内容。
          摘要可以跨越多行。

        # -- 格式与排版 --
        lang: "zh-CN" # 文档主语言 (影响断词、引用格式等)
        fontsize: 12pt
        geometry:
          - "top=3cm, bottom=3cm, left=2.5cm, right=2.5cm"
        mainfont: "Times New Roman"
        monofont: "Courier New"
        CJKmainfont: "SimSun" # 中文字体 (宋体)
        CJKmonofont: "SimHei" # 中文等宽字体 (黑体)
        
        # -- 目录设置 --
        toc: true # `true` 来生成目录
        toc-depth: 3 # 目录深度
        
        # -- 引用与文献 --
        # 在下方指定你的 CSL 样式文件和 .bib 文件
        # 可通过 `paw csl use <样式名>` 命令来设置
        csl: gbt7714-author-date.csl
        bibliography: resources/bibliography.bib
        link-citations: true # 为文内引用添加链接

        # -- Word 文档模板 --
        # 可通过 `paw template use <模板名>` 命令来设置
        # reference-doc: your-template.docx

        # -- 交叉引用与编号 --
        # 使用 pandoc-crossref 过滤器来启用交叉引用
        # 过滤器需要在命令行中通过 `-F pandoc-crossref` 启用 (Makefile已配置)
        # 图表标题格式: ![Caption.](./figures/figure.png){{{{ #fig:label }}}}
        # 表格标题格式: : Caption. {{{{ #tbl:label }}}}
        # 公式格式: $$ a^2+b^2=c^2 $$ {{{{ #eq:label }}}}
        # 引用方式: [@fig:label], [@tbl:label], [@eq:label]
        figPrefix: "图"
        tblPrefix: "表"
        eqPrefix: "公式"
        
        # -- PDF 渲染引擎 --
        # 默认使用 pdflatex, 如果需要支持中文, 请确保安装了支持中文的 LaTeX 发行版 (如 TeX Live)
        # 并且通常需要使用 xelatex 引擎
        # pdf-engine: xelatex
        ---

        <!-- 
        此文件用于定义整篇论文的元数据。
        Pandoc 会在编译时读取这些配置。
        正文内容请在 01-introduction.md 等文件中编写。
        -->
    ''').strip()


def get_introduction_template() -> str:
    return textwrap.dedent('''
        # 引言

        在这里开始你的第一章。
    ''').strip()


def get_gitignore_template() -> str:
    return textwrap.dedent('''
        # PAW 生成的 .gitignore

        # 忽略编译输出目录
        /output/

        # Python 缓存与临时文件
        __pycache__/
        *.py[cod]
        *$py.class

        # 虚拟环境目录
        .venv/
        venv/
        ENV/

        # 编辑器与系统文件
        .vscode/
        .idea/
        .DS_Store
        *.swp
        
        # PAW 全局资源库 (不应在项目内)
        .paw/
    ''').strip()


def get_readme_template(project_name: str) -> str:
    return textwrap.dedent(f'''
        # {project_name}

        本项目由 PAW (Pandoc Academic Workflow) 创建。

        ## 项目结构

        - `manuscript/`: 存放你所有的 `.md` 稿件文件。
        - `resources/`: 存放引文样式 `.csl`、参考文献 `.bib` 和 Word 模板 `.docx` 等资源文件。
        - `figures/`: 存放所有图片文件。
        - `output/`: 存放最终编译生成的 `.pdf` 和 `.docx` 文件。
        - `Makefile`: 自动化编译脚本。

        ## 工作流程

        1.  **编写内容**: 在 `manuscript/` 文件夹中编写你的 Markdown 文件。文件名以 `数字-` 开头以确保编译顺序，例如 `01-introduction.md`, `02-related-work.md`。
        2.  **管理资源**:
            - 使用 `paw csl add <样式文件.csl>` 将你常用的 CSL 文件添加到全局库。
            - 在项目根目录，运行 `paw csl use <样式名>` 来使用并配置一个全局 CSL 样式。
            - `paw template` 命令同理。
        3.  **添加文献**: 使用 Zotero 等工具将参考文献导出到 `resources/bibliography.bib` 文件中。
        4.  **编译文档**: 在项目根目录下，打开终端，运行以下命令：
            - `make`: 同时生成 PDF 和 DOCX 格式的文档。
            - `make pdf`: 仅生成 PDF 文档。
            - `make docx`: 仅生成 DOCX 文档。
        5.  **清理输出**:
            - `make clean`: 删除 `output/` 目录下的所有文件。

        祝你写作顺利！
    ''').strip()


def get_makefile_template() -> str:
    return textwrap.dedent('''
        # ==============================================================================
        # PAW (Pandoc Academic Workflow) 生成的 Makefile - v0.5
        # ==============================================================================
        #
        # 此版本已简化, 它完全信赖 Pandoc 从 YAML frontmatter 中读取
        # `csl`, `bibliography`, 和 `reference-doc` 等配置。

        # --- 用户可配置变量 ---
        DOC_NAME = paper
        SRC_DIR = manuscript
        OUT_DIR = output
        RES_DIR = resources

        # --- 自动检测变量 ---
        CHAPTERS := $(shell find $(SRC_DIR) -name '[0-9]*.md' | sort)
        PANDOC = pandoc

        # --- Pandoc 编译参数 ---
        # 智能资源路径: Pandoc 会按顺序在项目根目录、`resources`目录和PAW全局资源库中查找文件
        # 这使得 CSL 和 Word 模板既可以项目本地化,也可以全局共享
        PANDOC_RESOURCE_PATHS = --resource-path=.:$(RES_DIR):$(HOME)/.paw/csl:$(HOME)/.paw/templates

        # 过滤器: 启用 pandoc-crossref 实现图、表、公式的交叉引用
        PANDOC_FILTERS = -F pandoc-crossref

        # 文献处理: 启用 citeproc 来处理参考文献和引用格式
        PANDOC_CITEPROC = --citeproc

        # PDF 引擎: 推荐使用 xelatex 以获得最佳的中文支持
        PDF_ENGINE = --pdf-engine=xelatex
        
        PANDOC_FLAGS = $(PANDOC_RESOURCE_PATHS) $(PANDOC_FILTERS) $(PANDOC_CITEPROC)

        # --- 定义目标 ---
        .PHONY: all pdf docx clean

        all: pdf docx

        pdf: $(OUT_DIR)/$(DOC_NAME).pdf
        docx: $(OUT_DIR)/$(DOC_NAME).docx

        # --- 定义规则 ---
        $(OUT_DIR):
        	@mkdir -p $(OUT_DIR)

        $(OUT_DIR)/$(DOC_NAME).pdf: $(CHAPTERS) | $(OUT_DIR)
        	@echo " brewing PDF..."
        	@$(PANDOC) $(PANDOC_FLAGS) $(PDF_ENGINE) -o $@ $(CHAPTERS)

        $(OUT_DIR)/$(DOC_NAME).docx: $(CHAPTERS) | $(OUT_DIR)
        	@echo " baking DOCX..."
        	@$(PANDOC) $(PANDOC_FLAGS) -o $@ $(CHAPTERS)

        clean:
        	@echo " cleaning output directory..."
        	@rm -rf $(OUT_DIR)/*

    ''').strip()