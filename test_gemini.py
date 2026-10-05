import sys
from app.config import settings
from app.gemini_service import gemini_service


def main():
  print("=" * 50)
  print("🤖 Google Gemini API 連線測試")
  print("=" * 50)

  if not settings.GEMINI_API_KEY:
    print(
        "❌ 尚未偵測到 GEMINI_API_KEY！\n"
        "👉 請先在專案根目錄建立 .env 檔案並填入你的金鑰，例如：\n"
        "   GEMINI_API_KEY=AIzaSy...\n"
    )
    sys.exit(1)

  prompt = "請用繁體中文以熱情的口吻，向第一次使用 LINE 機器人的使用者打招呼！"
  print(f"📝 測試發送提示詞: {prompt}\n")
  print("⏳ 正在向 Gemini 請求回覆...")

  reply = gemini_service.generate_reply(prompt)
  print("\n✅ 收到 Gemini 回覆如下：")
  print("-" * 50)
  print(reply)
  print("-" * 50)


if __name__ == "__main__":
  main()
