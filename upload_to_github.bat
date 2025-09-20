@echo off
echo ========================================
echo YEAP Dashboard - GitHub Upload Script
echo ========================================
echo.

REM 检查是否在正确的目录
if not exist "streamlit" (
    echo Error: Please run this script from the YEAP-9-19 project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Adding all changes to Git...
git add .
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to add files to Git
    pause
    exit /b 1
)
echo Files added successfully!
echo.

echo Step 3: Committing changes...
set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" set commit_message=Update YEAP Dashboard - %date% %time%

git commit -m "%commit_message%"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to commit changes
    pause
    exit /b 1
)
echo Changes committed successfully!
echo.

echo Step 4: Pushing to GitHub...
echo Attempting normal push first...
git push origin main
if %ERRORLEVEL% neq 0 (
    echo Normal push failed, trying force push...
    echo WARNING: This will overwrite remote changes!
    set /p confirm="Continue with force push? (y/N): "
    if /i "%confirm%"=="y" (
        git push origin main --force
        if %ERRORLEVEL% neq 0 (
            echo Error: Force push also failed
            echo Please check your internet connection and GitHub credentials
            pause
            exit /b 1
        )
        echo Force push completed successfully!
    ) else (
        echo Push cancelled by user
        pause
        exit /b 1
    )
) else (
    echo Push completed successfully!
)
echo.

echo ========================================
echo Upload completed successfully!
echo Your YEAP Dashboard has been uploaded to:
echo https://github.com/50281Github/YEAP-Dashboard.git
echo ========================================
echo.
echo Streamlit Cloud should automatically update within a few minutes.
echo You can check the deployment status at:
echo https://share.streamlit.io/
echo.
pause