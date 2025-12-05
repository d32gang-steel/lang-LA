# LangGraph 线性代数助教系统

一个基于 LangGraph 的多 Agent 线性代数教学助手系统，包含计算和可视化功能。

## 项目简介

本项目是一个智能线性代数助教系统，通过多个专门的 Agent 来帮助学生理解和解决线性代数问题：

- **计算 Agent** (`compute_agent.py`): 使用 NumPy 进行线性代数计算
- **可视化 Agent** (`visual_agent.py`): 可视化 2D 线性变换
- **苏格拉底式教学 Agent** (`socratic_agent.py`): 通过提问引导学生学习

## 项目结构

```
lang-LA/
├── src/                      # Python Agent 源代码
│   ├── compute_agent.py     # 计算 Agent
│   ├── visual_agent.py      # 可视化 Agent
│   └── socratic_agent.py    # 苏格拉底式教学 Agent
├── agent-chat-ui/           # Next.js 前端界面
├── langgraph.json           # LangGraph 配置文件
├── requirements.txt         # Python 依赖
└── README.md               # 项目说明文档
```

## 功能特性

### 计算 Agent
- 使用 NumPy 进行线性代数计算
- 支持矩阵运算、向量计算等
- 基于 Gemini-2.5-Pro 模型
- **支持图片输入**：可以读取用户上传的图片中的数学内容

### 可视化 Agent
- 可视化 2x2 矩阵对单位正方形的线性变换
- 生成 Base64 编码的 PNG 图像
- 基于 Gemini-2.5-Pro 模型
- **支持图片输入**：可以读取用户上传的图片中的数学内容

### 苏格拉底式教学 Agent
- 通过提问引导学生自主发现答案
- 不直接给答案，而是引导思考
- 记录学习点，提供个性化指导
- 基于 Gemini-2.5-Pro 模型
- **支持图片输入**：可以读取用户上传的图片中的数学内容

## 环境要求

- Python 3.8+
- Node.js 18+ (用于前端)
- pnpm (用于前端包管理)

## 安装步骤

### 1. 克隆仓库

```bash
git clone <repository-url>
cd lang-LA
```

### 2. 创建并激活虚拟环境（推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件，添加以下配置：

```env
API_KEY=your_api_key_here
API_BASE_URL=your_api_base_url_here
```

**注意**: `API_BASE_URL` 应该指向你的 API 服务地址。如果 URL 不以 `/v1` 结尾，系统会自动添加。

### 5. 安装前端依赖（可选）

如果你需要运行前端界面：

```bash
cd agent-chat-ui
pnpm install
```

## 使用方法

### 1. 启动 LangGraph 后端服务

**重要**：必须先启动后端服务，前端才能正常工作。

在项目根目录运行：

```bash
langgraph dev
```

这将启动 LangGraph 服务，默认运行在 `http://127.0.0.1:2024`。

启动后会显示：
- 🚀 **API**: `http://127.0.0.1:2024`
- 🎨 **Studio UI**: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`
- 📚 **API Docs**: `http://127.0.0.1:2024/docs`

**注意**：
- 确保已激活虚拟环境并安装了所有 Python 依赖
- **LangGraph Studio UI** 是 LangGraph 自带的 Web 界面，可以直接在浏览器中使用，无需单独启动前端
- Studio UI 中可能已经有切换 Agent 的功能

### 2. 配置前端环境变量（可选）

在 `agent-chat-ui` 目录下创建 `.env.local` 文件：

```bash
cd agent-chat-ui
```

创建 `.env.local` 文件，添加以下配置：

```env
# LangGraph 后端服务地址（本地开发）
LANGGRAPH_API_URL=http://127.0.0.1:2024

# LangSmith API Key（如果需要）
LANGSMITH_API_KEY=your_langsmith_api_key_here

# 前端 API 代理地址（本地开发）
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# 使用的 Agent ID（从 langgraph.json 中选择）
NEXT_PUBLIC_ASSISTANT_ID=compute-agent
```

**注意**：
- `LANGGRAPH_API_URL` 必须指向运行 `langgraph dev` 的地址（默认是 `http://127.0.0.1:2024`）
- `NEXT_PUBLIC_ASSISTANT_ID` 可以是 `compute-agent`、`visual-agent` 或 `socratic-agent`（根据 `langgraph.json` 中定义的 Agent）

### 3. 启动前端界面（可选）

**方式一：使用 LangGraph Studio UI（推荐，无需额外配置）**

直接访问启动后端时显示的 Studio UI 链接：
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

这是 LangGraph 自带的 Web 界面，可以直接使用，通常已经包含 Agent 切换功能。

**方式二：使用自定义前端应用**

如果你想使用自定义的聊天界面，在 `agent-chat-ui` 目录下运行：

```bash
cd agent-chat-ui
pnpm dev
```

前端界面将在 `http://localhost:3000` 启动。

### Agent 切换

**在自定义前端界面中**，右上角提供了 **Agent 选择器**，你可以直接在界面上切换不同的 Agent：

- **计算助手** (`compute-agent`): 执行线性代数计算
- **可视化助手** (`visual-agent`): 生成线性变换图像
- **苏格拉底式教学** (`socratic-agent`): 通过提问引导学习

切换 Agent 时会自动重置当前对话，因为不同 Agent 的对话历史是独立的。

### 启动顺序总结

1. ✅ 启动后端：`langgraph dev`（在项目根目录）
2. ✅ 配置前端：创建 `agent-chat-ui/.env.local` 文件（如果使用自定义前端）
3. ✅ 启动前端：`cd agent-chat-ui && pnpm dev`（如果使用自定义前端）

## Agent 说明

### Compute Agent

计算 Agent 专门用于执行线性代数计算任务。它使用 `python_math_tool` 工具来执行 NumPy 计算。

**使用示例**:
- 矩阵乘法
- 矩阵求逆
- 特征值计算
- 向量运算

**图片支持**：
- 如果用户上传了包含数学内容的图片（矩阵、公式、题目等），Agent 可以读取图片内容
- 然后根据图片中的内容使用 `python_math_tool` 进行计算
- 结合图片内容和计算结果给出完整的回答

### Visual Agent

可视化 Agent 用于生成线性变换的可视化图像。它使用 `plot_2d_transformation` 工具来创建 2D 变换图。

**使用示例**:
- 输入: `[[1, 2], [0, 1]]` (2x2 矩阵的 JSON 字符串)
- 输出: Base64 编码的 PNG 图像，展示矩阵对单位正方形的变换效果

**图片支持**：
- 如果用户上传了图片，Agent 可以读取和分析图片中的数学内容（矩阵、公式、图形等）
- 然后根据图片内容生成相应的可视化

### Socratic Agent

苏格拉底式教学 Agent，通过提问引导学生自主发现答案，而不是直接给出解答。它使用以下工具：
- `analyze_student_response`: 分析学生回答的质量和理解程度
- `record_learning_point`: 记录学生的学习点和困惑点

**教学特点**:
- 提问引导，不直接给答案
- 循序渐进，由浅入深
- 鼓励发现，体验"啊哈"时刻
- 及时反馈，调整策略

**使用场景**:
- 学生需要理解概念而非直接计算
- 需要培养数学思维和推理能力
- 通过对话式学习加深理解

**图片支持**：
- 如果学生上传了图片（题目、公式、解题过程等），Agent 可以读取图片内容
- 根据图片中的内容进行提问引导
- 结合图片和文字问题一起分析，帮助学生理解

## 配置说明

`langgraph.json` 文件定义了可用的 Agent：

```json
{
  "graphs": {
    "compute-agent": "./src/compute_agent.py:agent",
    "visual-agent": "./src/visual_agent.py:agent",
    "socratic-agent": "./src/socratic_agent.py:agent"
  }
}
```

## 技术栈

### 后端
- **LangChain**: Agent 框架
- **LangGraph**: 多 Agent 编排
- **NumPy**: 数值计算
- **Matplotlib**: 数据可视化
- **Gemini-2.5-Pro**: 支持多模态（文本+图片）的 LLM

### 前端
- **Next.js**: React 框架
- **TypeScript**: 类型安全
- **Tailwind CSS**: 样式框架
- **LangGraph SDK**: LangGraph 客户端

## 图片输入功能

所有 Agent 都使用 **Gemini-2.5-Pro** 模型，支持图片输入功能：

1. **前端支持**：前端界面支持上传图片（JPEG、PNG、GIF、WEBP、PDF）
2. **自动处理**：LangChain 会自动将图片转换为模型 API 需要的格式
3. **模型支持**：Gemini-2.5-Pro 原生支持视觉理解，可以读取和分析图片内容

**使用方法**：
- 在聊天界面中点击上传按钮或拖拽图片
- 输入你的问题（可选）
- Agent 会分析图片内容并结合你的问题给出回答

## 开发说明

### 添加新的 Agent

1. 在 `src/` 目录下创建新的 Python 文件
2. 定义 Agent 和工具
3. 在 `langgraph.json` 中添加配置
4. 确保导出的 Agent 变量名为 `agent`

### 调试

- 确保 `.env` 文件配置正确
- 检查 API 服务是否可访问
- 查看 LangGraph 日志输出

## 许可证

请查看项目根目录的 LICENSE 文件（如果存在）。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 Issue 反馈。

