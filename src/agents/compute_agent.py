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

llm = ChatOpenAI(model="DeepSeek-V3.2-Exp", temperature=0, api_key=API_KEY, base_url=API_BASE_URL)
tools = [python_math_tool]
system_prompt = "你是一个线性代数助教。你必须使用 python_math_tool 来回答任何计算问题。"

# 创建并暴露 'agent' 变量
# CLI 将会自动寻找这个名为 'agent' 的变量
agent = create_agent(llm, tools, system_prompt=system_prompt)