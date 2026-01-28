import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

# 1. 加载环境变量 (.env 文件)
load_dotenv()

# 配置 Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# 配置 Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
notion = Client(auth=NOTION_TOKEN)

# 2. 初始化模型
model = genai.GenerativeModel(
    model_name="gemini-flash-latest"
)

def save_to_notion(task_data):
    """将数据写入 Notion 数据库"""
    try:
        # 这里的 Key (Name, Minutes, Category) 必须和你 Notion 表头完全一致
        new_page = {
            "Name": {"title": [{"text": {"content": task_data['task']}}]},
            "Minutes": {"number": task_data['minutes']},
            "Category": {"select": {"name": task_data['category'].capitalize()}},
            "Date": {"date": {"start": datetime.now().isoformat()}}
        }
        notion.pages.create(parent={"database_id": DATABASE_ID}, properties=new_page)
        print(f"✅ [Notion] Successfully recorded: {task_data['task']}")
    except Exception as e:
        print(f"❌ [Notion] Sync failed: {e}")

def check_available_models():
    print("\n🔍 Checking available models for your API Key...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
    except Exception as e:
        print(f"   ❌ Could not list models: {e}")

def parse_and_sync(user_input):
    try:
        # 将系统指令直接整合到 Prompt 中，确保 gemini-pro 能理解
        prompt = (
            "You are a focus coach. Convert vague user input into JSON format. "
            "Must include the following fields: "
            "1. task (string): Task name "
            "2. minutes (int): Duration in minutes "
            "3. category (string): Must be one of Work, Study, Fitness, Life, Entertainment.\n\n"
            f"User Input: {user_input}"
        )
        # 调用 Gemini 解析
        response = model.generate_content(prompt)
        # Clean up markdown formatting (```json ... ```) commonly returned by gemini-pro
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        task_data = json.loads(clean_text)
        
        print("💎 AI Parse Result:")
        print(json.dumps(task_data, indent=4, ensure_ascii=False))
        
        # 核心逻辑：解析成功后直接同步到 Notion
        save_to_notion(task_data)
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        if "404" in str(e):
            print("⚠️ It seems the model name is invalid or not available.")
            check_available_models()

# 3. 交互主循环
if __name__ == "__main__":
    if not all([API_KEY, NOTION_TOKEN, DATABASE_ID]):
        print("❌ Error: Please check .env file, ensure GEMINI_API_KEY, NOTION_TOKEN and NOTION_DATABASE_ID are configured.")
    else:
        print("🧘 FocusPulse is ready (Type 'exit' to quit)")
        try:
            while True:
                user_input = input("\nWhat do you want to focus on? ")
                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Keep Calm and Focus!")
                    break
                if not user_input.strip():
                    continue
                
                parse_and_sync(user_input)
        except KeyboardInterrupt:
            print("\n👋 Keep Calm and Focus! (Interrupted)")