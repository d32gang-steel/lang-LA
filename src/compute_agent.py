import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import numpy as np

# 定义一个使用 NumPy 进行线性代数计算的工具
@tool
def python_math_tool(query: str) -> str:
    """一个使用 NumPy 和 Python 来解决线性代数问题的工具。"""
    try:
        local_vars = {"np": np}
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            exec(query, {"np": np}, local_vars)
        s = f.getvalue()
        return f"计算成功:\n{s}"
    except Exception as e:
        return f"代码执行出错: {str(e)}"

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

llm = ChatOpenAI(model="gemini-2.5-pro", temperature=0, api_key=API_KEY, base_url=API_BASE_URL)
tools = [python_math_tool]
system_prompt = """你是一个线性代数助教。你必须使用 python_math_tool 来回答任何计算问题。

**图片支持**：
- 如果用户上传了包含数学内容的图片（矩阵、公式、题目等），你可以读取图片内容
- 然后根据图片中的内容使用 python_math_tool 进行计算
- 结合图片内容和计算结果给出完整的回答
"""

# 创建并暴露 'agent' 变量
# CLI 将会自动寻找这个名为 'agent' 的变量
agent = create_agent(llm, tools, system_prompt=system_prompt)