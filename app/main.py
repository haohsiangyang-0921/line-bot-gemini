import logging
from app.config import settings
from app.line_service import get_parser, handle_message_event
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from linebot.v3.exceptions import InvalidSignatureError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("line_bot_main")

app = FastAPI(
    title="LINE Gemini Bot API",
    description="以 FastAPI + Google Gemini API 打造的智慧 LINE 對話機器人",
    version="1.0.0",
)


@app.get("/")
def health_check():
  """健康檢查端點：回傳伺服器狀態與金鑰配置確認"""
  return {
      "status": "healthy",
      "service": "LINE Gemini Bot",
      "configured": {
          "line_secret": bool(settings.LINE_CHANNEL_SECRET),
          "line_access_token": bool(settings.LINE_CHANNEL_ACCESS_TOKEN),
          "gemini_api_key": bool(settings.GEMINI_API_KEY),
      },
  }


@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks):
  """LINE Webhook 回調接收端點：驗證簽章並進行非同步事件分發"""
  signature = request.headers.get("X-Line-Signature", "")
  body = (await request.body()).decode("utf-8")

  if not settings.LINE_CHANNEL_SECRET:
    logger.error("尚未設定 LINE_CHANNEL_SECRET，無法進行簽章比對！")
    raise HTTPException(
        status_code=500, detail="Server LINE secret is not configured"
    )

  try:
    parser = get_parser()
    events = parser.parse(body, signature)
  except InvalidSignatureError:
    logger.warning("收到無效的 LINE 簽章 (InvalidSignatureError)！")
    raise HTTPException(status_code=400, detail="Invalid signature")
  except Exception as e:
    logger.error(f"解析 Webhook 事件失敗: {e}")
    raise HTTPException(status_code=400, detail=str(e))

  # 使用背景任務異步處理，確保在 LINE 限制時間內快速回傳 200 OK
  for event in events:
    background_tasks.add_task(handle_message_event, event)

  return JSONResponse(content={"status": "OK"})


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
