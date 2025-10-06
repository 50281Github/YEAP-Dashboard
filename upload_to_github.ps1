# YEAP Dashboard - GitHub Upload Script (PowerShell Version)
# Usage: Right-click project folder -> "Open PowerShell window here" -> Run .\upload_to_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YEAP Dashboard - GitHub Upload Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "streamlit")) {
    Write-Host "Error: Please run this script from the YEAP-9-19 project root directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    # Step 1: Check Git status
    Write-Host "Step 1: Checking Git status..." -ForegroundColor Green
    git status
    Write-Host ""

    # Step 2: Add all changes
    Write-Host "Step 2: Adding all changes to Git..." -ForegroundColor Green
    git add .
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to add files to Git"
    }
    Write-Host "Files added successfully!" -ForegroundColor Green
    Write-Host ""

    # Step 3: Commit changes
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

    # Step 4: Push to GitHub
    Write-Host "Step 4: Pushing to GitHub..." -ForegroundColor Green
    Write-Host "Attempting normal push first..." -ForegroundColor Yellow
    
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Normal push failed, trying force push..." -ForegroundColor Yellow
        Write-Host "WARNING: This will overwrite remote changes!" -ForegroundColor Red
        
        $confirm = "y"
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

    # Success completion
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