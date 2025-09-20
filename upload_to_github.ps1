# YEAP Dashboard - GitHub Upload Script (PowerShell Version)
# 使用方法: 在项目根目录右键 -> "在此处打开PowerShell窗口" -> 运行 .\upload_to_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YEAP Dashboard - GitHub Upload Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在正确的目录
if (-not (Test-Path "streamlit")) {
    Write-Host "Error: Please run this script from the YEAP-9-19 project root directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    # Step 1: 检查Git状态
    Write-Host "Step 1: Checking Git status..." -ForegroundColor Green
    git status
    Write-Host ""

    # Step 2: 添加所有更改
    Write-Host "Step 2: Adding all changes to Git..." -ForegroundColor Green
    git add .
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to add files to Git"
    }
    Write-Host "Files added successfully!" -ForegroundColor Green
    Write-Host ""

    # Step 3: 提交更改
    Write-Host "Step 3: Committing changes..." -ForegroundColor Green
    $commitMessage = Read-Host "Enter commit message (or press Enter for default)"
    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $commitMessage = "Update YEAP Dashboard - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }

    git commit -m $commitMessage
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to commit changes"
    }
    Write-Host "Changes committed successfully!" -ForegroundColor Green
    Write-Host ""

    # Step 4: 推送到GitHub
    Write-Host "Step 4: Pushing to GitHub..." -ForegroundColor Green
    Write-Host "Attempting normal push first..." -ForegroundColor Yellow
    
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Normal push failed, trying force push..." -ForegroundColor Yellow
        Write-Host "WARNING: This will overwrite remote changes!" -ForegroundColor Red
        
        $confirm = Read-Host "Continue with force push? (y/N)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            git push origin main --force
            if ($LASTEXITCODE -ne 0) {
                throw "Force push also failed. Please check your internet connection and GitHub credentials"
            }
            Write-Host "Force push completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "Push cancelled by user" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    } else {
        Write-Host "Push completed successfully!" -ForegroundColor Green
    }
    Write-Host ""

    # 成功完成
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Upload completed successfully!" -ForegroundColor Green
    Write-Host "Your YEAP Dashboard has been uploaded to:" -ForegroundColor Green
    Write-Host "https://github.com/50281Github/YEAP-Dashboard.git" -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Streamlit Cloud should automatically update within a few minutes." -ForegroundColor Yellow
    Write-Host "You can check the deployment status at:" -ForegroundColor Yellow
    Write-Host "https://share.streamlit.io/" -ForegroundColor Blue
    Write-Host ""

} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Upload failed!" -ForegroundColor Red
}

Read-Host "Press Enter to exit"