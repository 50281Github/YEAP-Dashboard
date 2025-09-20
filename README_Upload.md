# GitHub 一键上传脚本使用说明

## 脚本文件说明

本项目提供了两个一键上传到GitHub的脚本：

### 1. `upload_to_github.bat` (批处理脚本)
- **适用于**: Windows系统
- **使用方法**: 双击运行
- **特点**: 简单易用，适合不熟悉命令行的用户

### 2. `upload_to_github.ps1` (PowerShell脚本)
- **适用于**: Windows PowerShell
- **使用方法**: 右键项目文件夹 → "在此处打开PowerShell窗口" → 输入 `.\upload_to_github.ps1`
- **特点**: 更好的错误处理和彩色输出

## 使用步骤

### 方法一：使用批处理脚本（推荐新手）
1. 确保你在 `YEAP-9-19` 项目根目录
2. 双击 `upload_to_github.bat` 文件
3. 按照提示操作：
   - 输入提交信息（可选，按回车使用默认信息）
   - 如果普通推送失败，选择是否强制推送

### 方法二：使用PowerShell脚本（推荐有经验用户）
1. 在项目根目录右键选择"在此处打开PowerShell窗口"
2. 输入命令：`.\upload_to_github.ps1`
3. 按照彩色提示操作

## 脚本功能

两个脚本都会自动执行以下操作：

1. **检查环境** - 确认在正确的项目目录
2. **查看状态** - 显示当前Git状态
3. **添加文件** - 将所有更改添加到Git (`git add .`)
4. **提交更改** - 提交到本地仓库 (`git commit`)
5. **推送到GitHub** - 上传到远程仓库 (`git push`)

## 安全特性

- ✅ **目录检查**: 确保在正确的项目目录运行
- ✅ **错误处理**: 每步都有错误检查和提示
- ✅ **用户确认**: 强制推送前会要求用户确认
- ✅ **详细日志**: 显示每步的执行结果

## 注意事项

### ⚠️ 重要提醒
- 脚本会上传**所有**当前目录的更改
- 如果普通推送失败，会提示是否使用强制推送
- 强制推送会**覆盖**GitHub上的远程更改

### 🔧 故障排除

**如果遇到推送失败：**
1. 检查网络连接
2. 确认GitHub凭据正确
3. 检查仓库权限

**如果脚本无法运行：**
1. 确保在项目根目录（包含`streamlit`文件夹）
2. 检查Git是否已安装并配置
3. 对于PowerShell脚本，可能需要修改执行策略：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## 成功后的结果

脚本成功运行后：
- ✅ 代码已上传到 GitHub 仓库
- ✅ Streamlit Cloud 会在几分钟内自动更新
- ✅ 可以在 https://share.streamlit.io/ 查看部署状态

## 手动上传（备用方法）

如果脚本无法使用，可以手动执行：
```bash
git add .
git commit -m "Update YEAP Dashboard"
git push origin main
```

---

**项目仓库**: https://github.com/50281Github/YEAP-Dashboard.git  
**Streamlit Cloud**: https://share.streamlit.io/