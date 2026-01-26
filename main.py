import google.generativeai as genai
import os
import json

# 1. 配置你的 API Key (建议存放在环境变量中)
API_KEY = "你的_GEMINI_API_KEY" 
genai.configure(api_key=API_KEY)

# 2. 初始化模型并设定系统指令 (这就是我们之前聊的那个系统提示词)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="你是一个专注力教练。将用户模糊的输入转化为 JSON 格式。包含 task, minutes, category (Work, Study, Fitness, Life, Entertainment)。输出必须严格为 JSON 且只包含 JSON。"
)

def parse_task(user_input):
    # 调用 Gemini
    response = model.generate_content(user_input)
    
    try:
        # 解析返回的 JSON 字符串
        task_data = json.loads(response.text)
        print("✅ 任务解析成功:")
        print(json.dumps(task_data, indent=4, ensure_ascii=False))
        return task_data
    except:
        print("❌ 解析失败，Gemini 返回了非 JSON 内容")
        print(response.text)

# 3. 测试一下
if __name__ == "__main__":
    test_input = "我要写代码写到下午五点，大概还有两小时"
    parse_task(test_input)