# YEAP Dashboard - 新手指南

本教程将指导您如何在本地设置 YEAP Dashboard 项目，将其上传到 GitHub，并部署到 Streamlit Cloud。

## 1. 前提条件

在开始之前，请确保您已安装并设置好以下各项：

- **Git**: 用于版本控制和与 GitHub 交互。
  - 下载地址: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Python : 仪表板的编程语言。
  - 下载地址: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Streamlit**: 用于构建仪表板的框架。
  - 通过 pip 安装: `pip install streamlit`
- **GitHub 账户**: 用于托管您的代码仓库。
  - 注册地址: [https://github.com/join](https://github.com/join)
- **Streamlit Cloud 账户**: 用于在线部署您的仪表板。
  - 注册地址: [https://streamlit.io/cloud](https://streamlit.io/cloud)

## 2. 本地设置

1.  **下载项目**: 获取项目文件（例如，通过下载 ZIP 文件或如果您已有仓库则克隆）。
    -   将项目解压到 `C:\Users\您的用户名\Desktop\YEAP-9-19` 等位置。

2.  **打开终端**: 在您的终端（Windows 上为 PowerShell）中导航到项目根目录 (`YEAP-9-19`)。
    -   在文件资源管理器中，右键单击 `YEAP-9-19` 文件夹内部，然后选择“在此处打开终端”或“在此处打开 PowerShell 窗口”。

3.  **安装依赖**: Streamlit 应用程序需要特定的 Python 库。这些库列在 `streamlit/requirements.txt` 中。
    -   激活环境（如果需要）：
        ```bash
        # 如果您使用的是特定的 Python 环境，请在此处激活它。
        # 例如：conda activate myenv 或 .\.venv\Scripts\Activate.ps1
        ```
    -   安装所需的包：
        ```bash
        pip install -r streamlit/requirements.txt
        ```

4.  **在本地运行仪表板**: 您可以使用 `start_dashboard.py` 脚本快速启动。
    -   确保您的虚拟环境已激活。
    -   运行脚本：
        ```bash
        python start_dashboard.py
        ```
    -   此脚本将自动在您的默认网页浏览器中打开 `http://localhost:8501`（或类似地址），您的仪表板将在此处运行。

## 3. 上传到 GitHub

本项目包含一个 PowerShell 脚本 (`upload_to_github.ps1`)，用于简化将代码上传到 GitHub 仓库的过程。

1.  **创建新的 GitHub 仓库**: 
    -   访问 [https://github.com/new](https://github.com/new)。
    -   选择一个仓库名称（例如，`YEAP-Dashboard`）。
    -   **重要**: 不要使用 README、.gitignore 或许可证初始化仓库。请将它们留空，因为您的项目已经包含这些文件。
    -   点击“创建仓库”。

2.  **在本地初始化 Git**: 如果您的项目文件夹尚未是 Git 仓库，您需要对其进行初始化。
    -   在 `YEAP-9-19` 项目根目录中打开终端。
    -   初始化 Git：
        ```bash
        git init
        ```

3.  **将本地仓库链接到 GitHub**: 将您的本地仓库连接到新创建的 GitHub 仓库。
    -   在您的 GitHub 仓库页面上，复制 HTTPS URL（例如，`https://github.com/您的用户名/YEAP-Dashboard.git`）。
    -   在您的终端中，添加远程源：
        ```bash
        git remote add origin https://github.com/您的用户名/YEAP-Dashboard.git
        # 将 您的用户名 和 YEAP-Dashboard 替换为您的实际 GitHub 用户名和仓库名称
        ```
    -   如果您之前已初始化 Git 并链接到其他远程仓库，您可能需要先删除旧的远程仓库：
        ```bash
        git remote remove origin
        git remote add origin https://github.com/您的用户名/YEAP-Dashboard.git
        ```

4.  **运行上传脚本**: 
    -   **重要**: 在运行脚本之前，请打开 `upload_to_github.ps1` 文件，并将文件末尾的 GitHub 仓库 URL `https://github.com/50281Github/YEAP-Dashboard.git` 替换为您自己仓库的实际 URL。
    -   确保您的终端位于 `YEAP-9-19` 项目根目录中。
    -   执行 PowerShell 脚本：
        ```bash
        .\upload_to_github.ps1
        ```
    -   脚本将执行以下操作：
        -   检查 Git 状态。
        -   将所有更改添加到 Git。
        -   提示您输入提交消息（您可以按 Enter 键使用默认消息）。
        -   尝试正常推送。如果失败（例如，由于远程更改），它将自动尝试强制推送。
        -   成功推送后，它将显示您的 GitHub 仓库 URL 和一个用于检查 Streamlit Cloud 部署状态的链接。

## 4. 部署到 Streamlit Cloud

Streamlit Cloud 可以轻松地直接从 GitHub 部署您的 Streamlit 应用程序。

1.  **访问 Streamlit Cloud**: 打开您的网页浏览器并访问 [https://share.streamlit.io/](https://share.streamlit.io/)。

2.  **登录**: 使用您的 GitHub 账户登录。

3.  **部署应用程序**: 
    -   点击“New app”（新应用）按钮（通常在右上角）。
    -   选择“From existing repo”（从现有仓库）。

4.  **配置部署**: 
    -   **Repository (仓库)**: 选择您刚刚上传的 GitHub 仓库（例如，`您的用户名/YEAP-Dashboard`）。
    -   **Branch (分支)**: 选择 `main`（或 `master`，取决于您仓库的默认分支）。
    -   **Main file path (主文件路径)**: 输入 `streamlit/streamlit_app.py`（这是您的 Streamlit 应用程序的主文件）。
    -   **Python version (Python 版本)**: 选择一个兼容的 Python 版本（例如，`3.9` 或 `3.10`）。
    -   **Advanced settings (高级设置) (可选)**:
        -   **Secrets (密钥)**: 如果您的应用程序使用任何 API 密钥或敏感信息，您可以在此处添加。对于本项目，除非您添加外部数据源，否则可能不需要。
        -   **Custom command (自定义命令)**: 对于标准的 Streamlit 应用程序，通常不需要此项。

5.  **部署！**: 点击“Deploy!”（部署！）按钮。

    -   Streamlit Cloud 将开始构建和部署您的应用程序。此过程可能需要几分钟。
    -   部署完成后，您将获得一个可共享的仪表板公共 URL。

## 5. 在 Trae AI 中运行仪表板 (面向开发者)

如果您在 Trae AI 环境中工作，您可以直接在 IDE 中使用 `start_dashboard.py` 脚本进行快速本地测试。

1.  **打开 `start_dashboard.py`**: 在 Trae AI 文件浏览器中，导航并打开 `start_dashboard.py`。

2.  **运行脚本**: 当 `start_dashboard.py` 打开时，点击编辑器右上角的“运行”按钮（通常是一个播放图标）。

3.  **预览**: Trae AI 将执行脚本，激活虚拟环境，如果需要则安装依赖，并启动 Streamlit 应用程序。然后它将提供一个预览 URL（例如，`http://localhost:8501`），您可以在浏览器中打开该 URL 以查看仪表板。

此脚本处理环境检查、依赖安装，并自动打开浏览器，方便开发。

---

就是这样！您现在已经成功在本地运行并部署了您的 YEAP Dashboard。