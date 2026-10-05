@echo off
chcp 65001 >nul
echo ==============================================
echo  啟動 LINE Gemini Bot 伺服器
echo ==============================================

if not exist .env (
    echo 【警告】尚未建立 .env 檔案！正在從 .env.example 複製...
    copy .env.example .env
    echo 請先在 .env 中填寫您的 LINE 與 Gemini API 金鑰後再重新啟動。
    pause
    exit /b
)

if exist venv\Scripts\activate (
    call venv\Scripts\activate
)

echo 正在啟動 FastAPI 服務 (http://localhost:8000)...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
