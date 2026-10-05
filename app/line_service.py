import logging
from app.config import settings
from app.gemini_service import gemini_service
from linebot.v3 import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

logger = logging.getLogger(__name__)


def get_parser() -> WebhookParser:
  """取得 WebhookParser 實例"""
  return WebhookParser(settings.LINE_CHANNEL_SECRET)


async def handle_message_event(event: MessageEvent):
  """處理使用者傳送的 LINE 訊息事件"""
  if not isinstance(event.message, TextMessageContent):
    logger.info(f"忽略非文字訊息事件: {type(event.message)}")
    return

  user_text = event.message.text.strip()
  logger.info(f"收到來自使用者之訊息: {user_text}")

  # 呼叫 Gemini AI 生成回覆
  ai_reply = gemini_service.generate_reply(user_text)

  # 若未配置 Access Token，僅在日誌輸出
  if not settings.LINE_CHANNEL_ACCESS_TOKEN:
    logger.warning("尚未設定 LINE_CHANNEL_ACCESS_TOKEN，無法發送回覆至 LINE！")
    return

  try:
    configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
    async with AsyncApiClient(configuration) as api_client:
      line_bot_api = AsyncMessagingApi(api_client)
      await line_bot_api.reply_message(
          ReplyMessageRequest(
              reply_token=event.reply_token,
              messages=[TextMessage(text=ai_reply)],
          )
      )
    logger.info("成功發送回覆訊息至 LINE！")
  except Exception as e:
    logger.exception(f"發送 LINE 回覆訊息失敗: {e}")
