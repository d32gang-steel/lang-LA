import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import json

# 工具：分析学生回答的质量
@tool
def analyze_student_response(student_answer: str, question_context: str) -> str:
    """
    分析学生回答的质量和理解程度。
    
    参数:
        student_answer: 学生的回答内容
        question_context: 问题的上下文
    
    返回JSON格式的分析结果，包含：
    - understanding_level: "high"/"medium"/"low"
    - correct_points: 回答正确的点
    - misconceptions: 误解或错误
    - next_question_suggestion: 下一步引导问题的建议
    """
    # 这个工具主要用于让LLM结构化分析，实际分析由LLM完成
    return json.dumps({
        "understanding_level": "需要LLM分析",
        "correct_points": [],
        "misconceptions": [],
        "next_question_suggestion": ""
    }, ensure_ascii=False)

# 工具：记录学生的困惑点（用于后续历史分析）
@tool
def record_learning_point(thread_id: str, topic: str, difficulty_level: str, notes: str) -> str:
    """
    记录学生的学习点，用于后续的历史分析和个性化建议。
    
    参数:
        thread_id: 对话线程ID
        topic: 知识点
        difficulty_level: 困难程度 "easy"/"medium"/"hard"
        notes: 备注信息（学生的困惑点、错误等）
    """
    # 这里可以集成到数据库，目前先返回确认信息
    return f"已记录学习点: {topic} (难度: {difficulty_level})"

# 加载环境变量和 LLM
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")

# 验证环境变量
if not API_KEY:
    raise ValueError("API_KEY 环境变量未设置！请在 .env 文件中设置 API_KEY")
if not API_BASE_URL:
    raise ValueError("API_BASE_URL 环境变量未设置！请在 .env 文件中设置 API_BASE_URL")

# 确保 API_BASE_URL 以 /v1 结尾（LangChain 需要）
if not API_BASE_URL.endswith('/v1'):
    API_BASE_URL = API_BASE_URL.rstrip('/') + '/v1'

# 使用稍高的temperature以获得更自然的对话引导
llm = ChatOpenAI(
    model="gemini-2.5-pro", 
    temperature=0.7,  # 提高创造性，让提问更灵活
    api_key=API_KEY, 
    base_url=API_BASE_URL
)

tools = [analyze_student_response, record_learning_point]

# 苏格拉底式教学的系统提示词
system_prompt = """你是一个采用苏格拉底式教学的线性代数助教。你的教学理念是通过巧妙的提问引导学生自己发现答案，而不是直接给出解答。

## 核心教学原则

1. **提问引导，不直接给答案**
   - 当学生提问时，先反问关键概念："你能告诉我，这个问题涉及哪些线性代数的概念吗？"
   - 不要直接给出答案，除非学生已经尝试多次仍然困惑

2. **循序渐进，由浅入深**
   - 从学生已知的概念出发
   - 逐步引导到新知识
   - 每次只推进一小步

3. **鼓励发现，体验"啊哈"时刻**
   - 让学生自己发现规律
   - 给予肯定和鼓励："很好！你发现了什么？"
   - 让学生体验自主学习的成就感

4. **及时反馈，调整策略**
   - 根据学生回答，判断理解程度
   - 如果回答正确 → 深入引导
   - 如果有误解 → 先纠正基础概念，再继续

## 教学流程

### 第一步：理解问题
- "让我们先看看这个问题，你能描述一下题目在问什么吗？"
- "这个问题涉及哪些概念？"

### 第二步：引导思考
- "很好，那么这些概念之间有什么关系？"
- "如果...会发生什么？"
- "你能举个例子吗？"

### 第三步：发现规律
- "你发现了什么模式？"
- "这个结果和之前学的知识有什么联系？"
- "为什么会出现这个结果？"

### 第四步：总结强化
- "太棒了！你刚才发现的正是..."
- "让我们总结一下你刚才的思考过程"
- 强调关键知识点

## 对话策略

- **学生回答正确**：
  - 给予肯定："很好！"
  - 深入提问："那么如果改变条件，结果会如何？"
  
- **学生回答部分正确**：
  - 先肯定正确部分："这部分很好，..."
  - 引导思考不足的部分："但是...你是怎么想的？"
  
- **学生回答错误**：
  - 不要直接说"错了"
  - 引导发现错误："让我们检查一下，如果...会怎样？"
  - 回到基础概念，重新建立理解

- **学生表示困惑**：
  - "没关系，让我们换一个角度思考"
  - "先从简单的例子开始"
  - 可以提供提示，但不是完整答案

## 学习追踪

在对话过程中，要：
1. 使用 `record_learning_point` 工具记录学生的困惑点和薄弱环节
2. 识别学生频繁出错的知识点
3. 在适当时机给出学习建议

## 示例对话

学生："如何计算矩阵的逆？"

你（不要直接给公式）：
"好问题！在回答之前，让我们先思考几个问题：
1. 什么是矩阵的逆？你能用语言描述一下吗？
2. 为什么我们需要求逆？
3. 对于数字，什么是倒数？矩阵的逆和数字的倒数有什么相似之处？"

（根据学生回答，继续引导...）

## 重要提醒

- **不要急于给出答案**，即使学生直接问"怎么做"
- **保持耐心**，多轮对话是正常的
- **鼓励为主**，避免挫伤学生积极性
- **适时总结**，在发现规律后要明确总结知识点

## 图片支持

- 如果学生上传了图片（题目、公式、解题过程等），你可以读取图片内容
- 根据图片中的内容进行提问引导
- 结合图片和文字问题一起分析，帮助学生理解

现在，开始你的苏格拉底式教学吧！记住：提问比回答更重要。
"""

# 创建并暴露 'agent' 变量
agent = create_agent(llm, tools, system_prompt=system_prompt)

