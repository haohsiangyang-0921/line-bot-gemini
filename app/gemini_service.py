import logging
from google import genai
from app.config import settings

logger = logging.getLogger(__name__)


class GeminiService:
  """Google Gemini AI 服務封裝類別"""

  def __init__(self):
    self.system_prompt = (
        "你是一個友善、專業、知識淵博的繁體中文 AI 智慧助理。"
        "請使用清晰易懂的排版回覆使用者的問題。"
        "若內容較多，請適當使用條列與標籤進行整理；適度加上 Emoji 增加親和力。"
    )
    self._client = None

  @property
  def client(self):
    """延遲初始化 Gemini Client，確保若尚未設定金鑰時不會造成啟動崩潰"""
    if self._client is None and settings.GEMINI_API_KEY:
      self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return self._client

  def generate_reply(self, prompt: str) -> str:
    """呼叫 Gemini 模型產生文字回覆"""
    if not settings.GEMINI_API_KEY:
      return (
          "【系統提示】尚未設定 GEMINI_API_KEY，請先在 .env 中填寫 Google"
          " Gemini API 金鑰！"
      )

    try:
      client = self.client
      response = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=prompt,
          config={"system_instruction": self.system_prompt},
      )
      text = response.text or "抱歉，目前暫時無法產生回應，請稍後再試。"

      # LINE 單則訊息長度限制為 5000 字元，保留安全緩衝區
      if len(text) > 4800:
        text = text[:4800] + "\n\n...(因訊息長度限制，已自動為您截斷)"

      return text
    except Exception as e:
      logger.exception(f"Gemini API 生成回覆時發生異常: {e}")
      return f"處理訊息時發生錯誤：{str(e)}"


gemini_service = GeminiService()
