import google.generativeai as genai
import os
import json

# 1. 配置你的 API Key (建议存放在环境变量中)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # 如果没有环境变量，请在这里填入你的真实 Key，否则会报错
    API_KEY = "你的_GEMINI_API_KEY" 

genai.configure(api_key=API_KEY)

# 2. 初始化模型并设定系统指令 (这就是我们之前聊的那个系统提示词)
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction="你是一个专注力教练。将用户模糊的输入转化为 JSON 格式。包含 task, minutes, category (Work, Study, Fitness, Life, Entertainment)。",
    generation_config={"response_mime_type": "application/json"}
)

def parse_task(user_input):
    try:
        # 调用 Gemini
        response = model.generate_content(user_input)
        
        # 解析返回的 JSON 字符串
        task_data = json.loads(response.text)
        print("✅ 任务解析成功:")
        print(json.dumps(task_data, indent=4, ensure_ascii=False))
        return task_data
    except Exception as e:
        print("❌ 执行失败")
        print(f"错误详情: {e}")
        
        if "404" in str(e):
            print("\n⚠️ 提示: 模型未找到。请尝试更新 SDK: pip3 install -U google-generativeai")
            print("当前可用模型:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f" - {m.name}")

# 3. 测试一下
if __name__ == "__main__":
    print("🧘 FocusPulse 专注力教练已启动 (输入 'exit' 或 'quit' 退出)")
    while True:
        user_input = input("\n请输入你的计划: ")
        if not user_input.strip():
            continue
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("👋 再见！")
            break
        parse_task(user_input)