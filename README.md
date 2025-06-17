[简体中文](https://github.com/KawaroX/paw-cli/blob/main/README-CN.md)

# **🐾 PAW: Pandoc Academic Workflow**

**PAW (Pandoc Academic Workflow)** is a command-line tool designed for you, aiming to provide a one-click, professional, text-based academic writing and management ecosystem powered by Pandoc.

### **🤔 What is PAW?**

In traditional academic writing, we are often bogged down by tedious formatting adjustments, chaotic citation management, and a hard-to-track version history. PAW was born to solve these pain points.  
Our core philosophy is the **"separation of content and style."** We believe writers should dedicate 100% of their energy to **thinking and creating**, not struggling in the mire of font sizes, line spacing, and citation formats.  
With PAW, you can:

- Compose using simple Markdown syntax, enjoying all the advantages of plain text.
- Generate professionally typeset .pdf and .docx documents with a single, simple command.
- Seamlessly connect with Zotero, saying goodbye to the era of manual citation management.
- Effortlessly manage your citation styles and Word templates, reusing them across different projects.
- Enjoy the convenience of version control (like Git), making every revision traceable.

PAW is your loyal academic companion. It handles all the complex technical details for you, allowing you to focus on what truly matters from the very first minute of writing.

### **✨ Core Features**

- **One-Click Project Scaffolding**: Use the `paw new` command to instantly generate a complete paper project with a standard directory structure, an automated build script, and preset configuration files.
- **Cross-Platform Built-in Compilation**: With `paw build`, easily compile your Markdown manuscript into professional .pdf and .docx formats on any operating system.
- **Global Resource Management**: Use `paw csl` and `paw template` to build your own global library of citation styles and Word templates, configuring once and sharing across all projects.
- **Seamless Citation Experience**:
  - Use `paw zotero` (or `paw z`) to bring up Zotero's citation picker with a single command.
  - Use `paw cite` to quickly search and insert citations from your project's local .bib files.
- **Efficient Content Helpers**: Commands like `paw add chapter`, `paw add figure`, and `paw add bib` make adding new sections, images, and bibliographies a breeze.
- **Intelligent Environment Check**: `paw check` automatically verifies if core dependencies like Pandoc and LaTeX are installed and provides guidance.
- **Fun Easter Eggs**: We've hidden some fun little easter eggs (try `paw meow` or `paw woof`) to bring a bit of joy to the arduous process of academic writing.

## **🚀 Installation Guide**

### **Step 1: Prerequisites**

Before installing PAW, please ensure you have the following two core pieces of software installed on your computer:

1. **Pandoc**: The core typesetting engine for PAW. You can download and install it from the [official Pandoc website](https://pandoc.org/installing.html).
2. **LaTeX Distribution (Optional, for PDF output only)**: If you need to generate high-quality PDF documents, you will need to install a LaTeX distribution.
   - **macOS**: [MacTeX](https://www.tug.org/mactex/) (approx. 5GB)
   - **Windows**: [MiKTeX](https://miktex.org/)
   - **Linux**: TeX Live (usually installed via your package manager, e.g., sudo apt-get install texlive-full)

_If you don't need to generate PDFs for now, you can skip installing LaTeX. PAW will still work perfectly to generate .docx files for you._

### **Step 2: Install PAW**

We offer two installation methods. Please choose one based on your network conditions.

#### **Method A: One-Liner Install (Recommended)**

This is the simplest and quickest way to install. Just open your terminal, copy the following command, and run it:

```bash
curl \-sSL https://raw.githubusercontent.com/KawaroX/paw-cli/main/install.sh | sudo \-E bash
```

What does this command do?  
It downloads the latest install.sh script from GitHub and executes it with sudo permissions. The script automatically detects your system, downloads the pre-compiled PAW application, and installs it to a standard system path, allowing you to use the paw command from anywhere.

#### **Method B: Manual Install (If the one-liner fails)**

If your network environment prevents the curl command from running smoothly, you can install PAW manually with these steps:

1. **Visit the GitHub Releases Page**:
   - Open our [PAW-CLI Releases page](https://github.com/KawaroX/paw-cli/releases).
2. **Download the Application Bundle**:
   - Find the latest release (e.g., v0.6.0).
   - In the "Assets" section, download the .tar.gz archive that matches your system. For an Apple Silicon Mac, you would download paw-v0.6.0-macos-arm64.tar.gz.
3. **Extract and Install**:
   - Open your terminal and navigate to your downloads directory (usually \~/Downloads).
   - Run the following commands to extract and install the application:

```bash
# 1. Extract the file, which creates a folder named 'paw'
tar \-xzf paw-v0.6.0-macos-arm64.tar.gz

# 2. Move the entire 'paw' folder to a standard location
# You will be prompted for your password
sudo mv paw /usr/local/opt/paw-cli

# 3. Create a symbolic link so you can use the 'paw' command directly
sudo ln \-sf /usr/local/opt/paw-cli/paw /usr/local/bin/paw
```

### **Step 3: Verify Installation**

Regardless of the method you used, once finished, please open a **new terminal window** and run:

```bash
paw --help
```

If it successfully displays the help message for PAW, the installation was a success! Next, run the environment check:

```
paw check
```

This will report the status of Pandoc and LaTeX on your system.

## **📖 Command Reference**

| Command                 | Description                                 | Aliases         |
| :---------------------- | :------------------------------------------ | :-------------- |
| paw new "Title"         | Creates a new academic project.             | chuangjian      |
| paw build               | Builds the project, generating all formats. | b               |
| paw check               | Checks for core dependencies.               | c, jiancha, dig |
| paw add chapter "Title" | Adds a new chapter to the project.          | chap, zhang     |
| paw add figure \<path\> | Adds a figure to the project.               | fig, tupian     |
| paw add bib \<path\>    | Adds a .bib file to the project.            | wenxian         |
| paw zotero              | Triggers the Zotero citation picker.        | z               |
| paw cite [keywords]     | Searches local .bib files.                  | yinyong, hunt   |
| paw csl list/add/rm/use | Manages the global CSL style library.       | style, yangshi  |
| paw template ...        | Manages the global Word template library.   | tmpl, moban     |
| paw shake               | Cleans the output/ directory.               |                 |
| paw meow                | Gets a random academic writing tip.         |                 |
| paw woof                | Shows project statistics.                   |                 |

## **Uninstalling PAW**

We also provide a one-liner script to safely and completely uninstall PAW.  
To uninstall PAW, run the following command in your terminal:

```bash
curl \-sSL https://raw.githubusercontent.com/KawaroX/paw-cli/main/uninstall.sh | sudo bash
```

The script will remove the main program and will ask for your confirmation before deleting the user data directory (~/.paw) where your CSL styles and templates are stored.

## **License**

This project is distributed under the **MIT** License.
