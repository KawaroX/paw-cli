[English](https://github.com/KawaroX/paw-cli/blob/main/README.md)

# **🐾 PAW: Pandoc Academic Workflow**

**PAW (Pandoc Academic Workflow)** 是一款为你量身打造的命令行工具，旨在提供一个一键式的、专业的、基于 Pandoc 和纯文本的学术写作与管理生态系统。

### **🤔 PAW 是什么？**

在传统的学术写作中，我们常常被繁琐的格式调整、混乱的文献管理和难以追踪的版本历史所困扰。PAW 的诞生，就是为了解决这些痛点。  
我们的核心理念是 **“内容与格式分离”**。我们相信，写作者应该将 100% 的精力投入到 **思考和创作** 本身，而不是在字号、行距和引用格式的泥潭中挣扎。  
通过 PAW，你可以：

- 使用简洁的 Markdown 语法进行创作，享受纯文本带来的所有优势。
- 通过简单的命令，一键生成符合专业排版规范的 PDF 和 .docx 文稿。
- 无缝连接 Zotero，告别手动管理参考文献的时代。
- 轻松管理你的引文样式和 Word 模板，在不同的项目中复用它们。
- 享受版本控制（如 Git）带来的便利，让你的每一个修改都有迹可循。

PAW 是你忠实的学术伴侣，它会为你处理所有繁杂的技术细节，让你能从写作的第一分钟起，就专注于真正重要的事情。

### **✨ 核心功能**

- **一键式项目创建**: 使用 `paw new` 命令，瞬间生成一个包含标准目录结构、自动化编译脚本和预设配置文件的完整论文项目。
- **跨平台的内置编译**: 使用 `paw build` 命令，在任何操作系统上都能轻松将你的 Markdown 文稿编译成专业的 .pdf 和 .docx 格式文档。
- **全局资源管理**: 通过 `paw csl` 和 `paw template` 命令，构建你自己的全局引文样式库和 Word 模板库，一次配置，所有项目共享。
- **无缝的引用体验**:
  - 使用 `paw zotero` (或 paw z)，一键唤出 Zotero 的文献选择器。
  - 使用 `paw cite`，快速在项目本地的 .bib 文件中搜索并插入引文。
- **高效的内容助手**: `paw add chapter`, `paw add figure`, `paw add bib` 等命令，让添加新章节、图片和参考文献变得轻而易举。
- **智能环境检查**: `paw check` 会自动检查你的电脑是否已安装 Pandoc 和 LaTeX 等核心依赖，并提供指引。
- **充满乐趣的彩蛋**: 我们在工具中埋下了一些有趣的彩蛋（试试 `paw meow` 或 `paw woof`），希望能为枯燥的学术写作带来一丝乐趣。

## **🚀 安装指南**

### **第一步：准备环境 (Prerequisites)**

在安装 PAW 之前，请确保你的电脑上已经安装了以下两个核心软件：

1. **Pandoc**: PAW 的核心排版引擎。你可以从 [Pandoc 官网](https://pandoc.org/installing.html) 下载并安装。
2. **LaTeX 发行版 (可选，仅用于生成 PDF)**: 如果你需要生成高质量的 PDF 文稿，你需要安装一个 LaTeX 发行版。
   - **macOS**: [MacTeX](https://www.tug.org/mactex/) (约 5GB)
   - **Windows**: [MiKTeX](https://miktex.org/)
   - **Linux**: TeX Live (通常通过你的包管理器安装，如 `sudo apt-get install texlive-full`)

_如果你暂时不需要生成 PDF，可以跳过安装 LaTeX。PAW 依然可以为你完美地生成 .docx 文件。_

### **第二步：安装 PAW**

我们提供两种安装方式，请根据你的网络情况选择。

#### **方法 A：一键式安装 (推荐)**

这是最简单、最快捷的安装方式。你只需要打开你的终端 (Terminal)，复制并运行以下命令：

```bash
curl \-sSL https://raw.githubusercontent.com/KawaroX/paw-cli/main/install.sh | sudo \-E bash
```

这条命令会做什么？  
它会从 GitHub 下载最新的 install.sh 安装脚本，并使用 sudo 权限来执行它。脚本会自动检测你的系统，下载预编译好的 PAW 应用程序，并将其安装到系统的标准路径，让你可以在任何地方直接使用 paw 命令。

#### **方法 B：手动安装 (当一键安装失败时)**

如果你的网络环境无法顺利执行上述 curl 命令，你可以通过以下步骤手动安装：

1. **访问 GitHub Releases 页面**:
   - 打开我们的 [PAW-CLI Releases 页面](https://github.com/KawaroX/paw-cli/releases)。
2. **下载应用程序包**:
   - 找到最新的版本（例如 v1.0.0）。
   - 在下方的 "Assets" 区域，下载与你系统匹配的 .tar.gz 压缩包。例如，对于 Apple Silicon Mac，你应该下载 paw-v1.0.0-macos-arm64.tar.gz。
3. **解压并安装**:

   - 打开终端，进入你存放下载文件的目录（通常是 \~/Downloads）。
   - 运行以下命令来解压和安装：

```bash
# 1. 解压文件，这会创建一个名为 'paw' 的文件夹
tar \-xzf paw-v1.0.0-macos-arm64.tar.gz

# 2. 将整个 'paw' 文件夹移动到标准安装位置
# 你需要输入你的电脑密码
sudo mv paw /usr/local/opt/paw-cli

# 3. 创建一个符号链接，让你可以直接使用 'paw' 命令
sudo ln \-sf /usr/local/opt/paw-cli/paw /usr/local/bin/paw
```

### **第三步：验证安装**

无论你使用哪种方式安装，完成后，请打开一个**全新的**终端窗口，运行：

```bash
paw --help
```

如果能成功显示 PAW 的帮助信息，说明你已安装成功！接着，运行环境检查：

```bash
paw check
```

它会告诉你 Pandoc 和 LaTeX 的状态。

## **📖 命令参考**

| 命令                    | 功能描述                 | 别名            |
| :---------------------- | :----------------------- | :-------------- |
| paw new "标题"          | 创建一个新项目。         | chuangjian      |
| paw build               | 编译项目，生成所有格式。 | b               |
| paw check               | 检查核心依赖。           | c, jiancha, dig |
| paw add chapter "标题"  | 添加一个新章节。         | chap, zhang     |
| paw add figure \<路径\> | 添加一张图片。           | fig, tupian     |
| paw add bib \<路径\>    | 向项目中添加 .bib 文件。 | wenxian         |
| paw zotero              | 触发 Zotero 搜索框。     | z               |
| paw cite \[关键词\]     | 搜索项目本地 .bib 文件。 | yinyong, hunt   |
| paw csl list/add/rm/use | 管理全局 CSL 样式。      | style, yangshi  |
| paw template ...        | 管理全局 Word 模板。     | tmpl, moban     |
| paw shake               | 清理 output/ 输出目录。  |                 |
| paw meow                | 获取一条随机写作小贴士。 |                 |
| paw woof                | 查看当前项目的统计信息。 |                 |

## **卸载 PAW**

我们同样提供一个一键式的卸载脚本，它可以安全、完整地移除 PAW。  
要卸载 PAW，请在终端运行以下命令：

```bash
curl \-sSL https://raw.githubusercontent.com/KawaroX/paw-cli/main/uninstall.sh | sudo bash
```

脚本会移除 PAW 的主程序，并询问你是否要一并删除存放 CSL 和模板的用户数据文件夹 (\~/.paw)。

## **许可证**

本项目基于 **MIT** 许可证分发。
