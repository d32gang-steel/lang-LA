# 文件: src/visual_agent.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import numpy as np

# ----------------- [ 关键修复 ] -----------------
# 1. 导入 matplotlib
import matplotlib
# 2. 强制使用 'Agg' 后端 (必须在 pyplot 导入之前！)
#    'Agg' 是一个非交互式后端，它只渲染到内存，不会创建窗口。
matplotlib.use('Agg')
# -----------------------------------------------

import matplotlib.pyplot as plt
import io
import base64

# --- 可视化 Agent 的专属工具 ---
@tool
def plot_2d_transformation(matrix_json: str) -> str:
    """
    接收一个代表 2x2 矩阵的 JSON 字符串（例如 "[[1, 2], [0, 1]]"），
    并可视化这个矩阵对单位正方形的线性变换。
    返回一个 Base64 编码的 PNG 图像字符串。
    """
    try:
        # 1. 解析输入
        import json
        matrix = np.array(json.loads(matrix_json))
        if matrix.shape != (2, 2):
            return "错误：矩阵必须是 2x2 的。"

        # 2. 设置绘图 (这一行之前会崩溃)
        fig, ax = plt.subplots()
        
        # 定义单位正方形
        unit_square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
        
        # 3. 计算变换
        transformed_square = unit_square @ matrix.T

        # 4. 绘制原始和变换后的图形
        ax.plot(unit_square[:, 0], unit_square[:, 1], 'b-', label='原始单位正方形')
        ax.plot(transformed_square[:, 0], transformed_square[:, 1], 'r-', label='变换后的图形')
        
        # 5. 设置坐标轴
        all_points = np.vstack([unit_square, transformed_square])
        max_val = np.abs(all_points).max() * 1.5
        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val, max_val)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True)
        ax.legend()
        ax.set_title(f'2D 线性变换: {matrix.tolist()}')

        # 6. 将图像保存到内存中的 Base64 字符串
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)  # 关闭图像，释放内存
        
        # 编码为 Base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return image_base64

    except Exception as e:
        plt.close('all') # 确保出错时关闭所有图像
        return f"绘图时出错: {str(e)}"

# --- 加载 LLM (和之前一样) ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")

llm = ChatOpenAI(model="gemini-2.5-pro", temperature=0, api_key=API_KEY, base_url=API_BASE_URL)
tools = [plot_2d_transformation]

# --- (关键) 升级 System Prompt 来处理图像 ---
system_prompt = """你是一个线性代数可视化助教。
你的任务是使用 plot_2d_transformation 工具来回答用户请求。

**重要规则**:
1.  你必须调用工具来生成图像。
2.  工具会返回一个 Base64 编码的字符串。
3.  在收到这个 Base64 字符串后，你 **必须** 将你的最终答案格式化为 Markdown 图像。
    
    格式如下:
    `![这是 {matrix_json} 的变换图像](data:image/png;base64,THE_BASE64_STRING_FROM_TOOL)`
    
    例如:
    `![这是 [[1, 2], [0, 1]] 的变换图像](data:image/png;base64,iVBORw0KGgo...)`
"""

# --- 暴露这个新的 Agent ---
agent = create_agent(llm, tools, system_prompt=system_prompt)