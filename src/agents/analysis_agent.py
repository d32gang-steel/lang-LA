import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import json
from datetime import datetime

# 添加项目根目录到路径，以便导入db模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from db import LearningPoint
except ImportError:
    # 如果导入失败，使用空实现（向后兼容）
    LearningPoint = None


@tool
def list_all_sessions() -> str:
    """
    列出所有有学习记录的会话，返回会话ID、记录数量、首次和最后记录时间。
    用户可以通过这个工具查看有哪些会话可供分析。
    """
    try:
        if LearningPoint is None:
            return json.dumps({"error": "数据库模块未配置"}, ensure_ascii=False)
        
        sessions = LearningPoint.get_all_sessions()
        return json.dumps(sessions, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": f"获取会话列表失败: {str(e)}"}, ensure_ascii=False)


@tool
def get_learning_statistics(thread_id: str) -> str:
    """
    获取指定线程的学习统计信息，包括总记录数、难度分布、常见困惑点等。
    
    参数:
        thread_id: 对话线程ID
    
    返回JSON格式的统计信息
    """
    try:
        if LearningPoint is None:
            return json.dumps({"error": "数据库模块未配置"}, ensure_ascii=False)
        
        stats = LearningPoint.get_statistics_by_thread(thread_id)
        return json.dumps(stats, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": f"获取统计数据失败: {str(e)}"}, ensure_ascii=False)


@tool
def get_recent_learning_points(thread_id: str, limit: int = 20) -> str:
    """
    获取指定线程的最近学习点记录。
    
    参数:
        thread_id: 对话线程ID
        limit: 返回的记录数量限制（默认20）
    
    返回JSON格式的学习点列表
    """
    try:
        if LearningPoint is None:
            return json.dumps({"error": "数据库模块未配置"}, ensure_ascii=False)
        
        points = LearningPoint.get_recent_learning_points(thread_id, limit)
        return json.dumps(points, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": f"获取学习点失败: {str(e)}"}, ensure_ascii=False)


@tool
def get_learning_points_by_topic(topic: str, limit: int = 50) -> str:
    """
    根据知识点获取相关的学习点记录（跨所有线程）。
    
    参数:
        topic: 知识点关键词
        limit: 返回的记录数量限制（默认50）
    
    返回JSON格式的学习点列表
    """
    try:
        if LearningPoint is None:
            return json.dumps({"error": "数据库模块未配置"}, ensure_ascii=False)
        
        points = LearningPoint.get_by_topic(topic, limit)
        return json.dumps(points, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": f"获取学习点失败: {str(e)}"}, ensure_ascii=False)


@tool
def analyze_learning_patterns(thread_id: str) -> str:
    """
    分析学生的学习模式和趋势，包括：
    - 困难点的时间分布
    - 知识点的掌握情况
    - 学习进度趋势
    
    参数:
        thread_id: 对话线程ID
    
    返回JSON格式的分析结果
    """
    try:
        if LearningPoint is None:
            return json.dumps({"error": "数据库模块未配置"}, ensure_ascii=False)
        
        # 获取所有学习点
        all_points = LearningPoint.get_by_thread_id(thread_id)
        
        if not all_points:
            return json.dumps({
                "message": "该线程暂无学习点记录",
                "suggestions": []
            }, ensure_ascii=False)
        
        # 统计困难点
        hard_points = [p for p in all_points if p['difficulty_level'] == 'hard']
        medium_points = [p for p in all_points if p['difficulty_level'] == 'medium']
        easy_points = [p for p in all_points if p['difficulty_level'] == 'easy']
        
        # 按主题统计
        topic_count = {}
        for point in all_points:
            topic = point['topic']
            if topic not in topic_count:
                topic_count[topic] = {'total': 0, 'hard': 0, 'medium': 0, 'easy': 0}
            topic_count[topic]['total'] += 1
            topic_count[topic][point['difficulty_level']] += 1
        
        # 找出最困难的 topic（hard 比例最高）
        difficult_topics = []
        for topic, counts in topic_count.items():
            if counts['total'] > 0:
                hard_ratio = counts['hard'] / counts['total']
                difficult_topics.append({
                    'topic': topic,
                    'hard_ratio': hard_ratio,
                    'total': counts['total'],
                    'hard_count': counts['hard']
                })
        
        difficult_topics.sort(key=lambda x: x['hard_ratio'], reverse=True)
        
        # 计算最近7天的活动
        now = datetime.now()
        recent_count = 0
        for point in all_points:
            created_at = point.get('created_at')
            if created_at is None:
                continue
            if isinstance(created_at, str):
                try:
                    created_at = datetime.strptime(created_at.split('.')[0], '%Y-%m-%d %H:%M:%S')
                except:
                    continue
            elif not isinstance(created_at, datetime):
                continue
            
            if created_at.tzinfo is not None:
                created_at = created_at.replace(tzinfo=None)
            if (now - created_at).days <= 7:
                recent_count += 1
        
        analysis = {
                "total_points": len(all_points),
                "difficulty_distribution": {
                    "hard": len(hard_points),
                    "medium": len(medium_points),
                    "easy": len(easy_points)
                },
            "difficult_topics": difficult_topics[:5],
                "recent_activity": recent_count
        }
        
        return json.dumps(analysis, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": f"分析学习模式失败: {str(e)}"}, ensure_ascii=False)


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

# 使用较低的temperature以获得更准确的分析
llm = ChatOpenAI(
    model="gemini-2.5-pro",
    temperature=0.3,  # 降低温度以获得更一致的分析结果
    api_key=API_KEY,
    base_url=API_BASE_URL,
    streaming=False  # 关闭流式输出避免闪烁
)

tools = [
    list_all_sessions,
    get_learning_statistics,
    get_recent_learning_points,
    get_learning_points_by_topic,
    analyze_learning_patterns
]

# 分析代理的系统提示词
system_prompt = """你是一个专业的学习分析助手，专门分析学生在线性代数学习过程中的历史数据，并提供个性化的学习建议。

## 核心功能

1. **历史数据分析**
   - 分析学生在不同知识点上的表现
   - 识别学生的薄弱环节和困难点
   - 追踪学习进度和趋势

2. **个性化建议**
   - 基于历史数据提供针对性的学习建议
   - 推荐需要重点复习的知识点
   - 制定学习计划和学习路径

3. **学习模式识别**
   - 识别学生的学习习惯和模式
   - 发现知识点的关联性
   - 预测可能的学习难点

## 使用工具

你可以使用以下工具来分析数据：

- `get_learning_statistics(thread_id)`: 获取学习统计信息（总记录数、难度分布、常见困惑点）
- `get_recent_learning_points(thread_id, limit)`: 获取最近的学习点记录
- `get_learning_points_by_topic(topic, limit)`: 根据知识点搜索相关记录
- `analyze_learning_patterns(thread_id)`: 深度分析学习模式和趋势

## 分析流程

### 1. 数据收集
当用户询问学习分析时：
- 首先使用 `get_learning_statistics` 获取整体概况
- 使用 `get_recent_learning_points` 查看最近的记录
- 如有需要，使用 `analyze_learning_patterns` 进行深度分析

### 2. 数据解读
- 解释统计数据的含义
- 指出关键的学习模式和趋势
- 识别需要关注的薄弱环节

### 3. 建议生成
基于分析结果提供：
- **短期建议**：立即需要关注的知识点
- **中期建议**：接下来1-2周的学习重点
- **长期建议**：整体学习路径的优化

## 回答风格

- **数据驱动**：所有建议都要基于实际的数据分析
- **具体明确**：避免泛泛而谈，要给出具体的知识点和行动建议
- **鼓励为主**：在指出问题的同时，也要肯定学生的进步
- **可执行**：建议要具体、可操作

## 示例回答结构

1. **当前状态总结**
   "根据你的学习记录，我发现..."

2. **关键发现**
   - 主要困难点
   - 学习趋势
   - 进步亮点

3. **个性化建议**
   - 需要重点复习的知识点
   - 建议的学习顺序
   - 学习方法建议

## 注意事项

- 如果某个线程没有学习记录，要友好地提示用户先进行学习
- 数据分析和建议要基于实际记录，不要凭空推测
- 当数据量较少时，可以说明分析的局限性
- 鼓励学生继续使用苏格拉底式教学代理来记录更多学习点

现在，开始为学生的学习提供专业的分析和建议吧！
"""

# 创建并暴露 'agent' 变量
agent = create_agent(llm, tools, system_prompt=system_prompt)

