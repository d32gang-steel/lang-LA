# Lang-LA：基于 LangChain 的线性代数 AI 助手

一个帮助学生学习线性代数的智能对话系统，结合了 Python 计算代理、可视化代理和现代化的聊天界面。

## ✨ 功能特点

- **计算代理**：使用 NumPy 解决线性代数计算问题
- **可视化代理**：将 2D 线性变换可视化，生成图像结果
- **聊天界面**：基于 Next.js 的现代化聊天 UI，支持流式响应
- **LangGraph 集成**：利用 LangGraph 管理代理工作流
- **多模型支持**：可配置 OpenAI、DeepSeek 等多种 LLM

## 🏗️ 技术栈

### 后端 (Python)

- **LangChain** + **LangGraph**：代理工作流框架
- **OpenAI API** / **DeepSeek**：大语言模型
- **NumPy**：数值计算
- **Matplotlib**：数据可视化
- **uv**：Python 包管理

### 前端 (Next.js)

- **Next.js 15**：React 框架
- **Tailwind CSS**：样式设计
- **LangGraph SDK**：与后端通信
- **TypeScript**：类型安全

## 🚀 快速开始

### 前提条件

- Python 3.13+ 和 uv（推荐）
- Node.js 18+ 和 pnpm

### 1. 克隆仓库

```bash
git clone git@github.com:d32gang-steel/lang-LA.git
cd lang-LA
```

### 2. 后端设置

```bash
# 进入后端目录
cd src

# 创建虚拟环境并安装依赖
uv venv
uv sync

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 设置环境变量（复制 .env.example 并填写）
copy .env.example .env
# 编辑 .env 文件，填入你的 API_KEY 和 API_BASE_URL（千万记得把中文注释删去，不然会报错）
```

### 3. 前端设置

```bash
# 返回项目根目录
cd ..

# 进入前端目录
cd agent-chat-ui

# 安装依赖
pnpm install

# 设置前端环境变量
copy .env.example .env
# 编辑 .env 文件，配置 NEXT_PUBLIC_API_URL 等
```

### 4. 启动服务

#### 方式一：分别启动（推荐开发）

```bash
# 终端1：启动 LangGraph 后端服务器
cd src
langgraph dev

# 终端2：启动前端开发服务器
cd agent-chat-ui
pnpm dev
```

#### 方式二：使用 Docker Compose（需要安装 Docker）

```bash
# 在项目根目录执行
docker-compose up -d
```

### 5. 访问应用

- 前端界面：`http://localhost:3000`
- LangGraph 服务器：`http://localhost:2024`

## 🔧 环境变量配置

### 后端 (.env 文件)

``` bash
API_KEY=your_openai_or_deepseek_api_key
API_BASE_URL=https://api.deepseek.com  # 或 OpenAI 地址
```

### 前端 (.env 文件)

``` bash
# 开发环境
NEXT_PUBLIC_API_URL=http://localhost:2024
NEXT_PUBLIC_ASSISTANT_ID=agent

# 生产环境
# NEXT_PUBLIC_API_URL=https://your-backend-domain.com
# LANGSMITH_API_KEY=your_langsmith_key  # 可选
```

## 📁 项目结构

``` text
lang-LA/
├── src/                    # Python 后端
│   ├── compute_agent.py   # 计算代理
│   ├── visual_agent.py    # 可视化代理
│   ├── pyproject.toml     # Python 依赖
│   └── .env.example       # 环境变量示例
├── agent-chat-ui/         # Next.js 前端
│   ├── src/app/           # 前端页面
│   ├── package.json       # Node.js 依赖
│   └── .env.example       # 前端环境变量示例
├── langgraph.json         # LangGraph 配置文件
└── README.md              # 本文档
```

---
**Happy Learning Linear Algebra with AI!**
