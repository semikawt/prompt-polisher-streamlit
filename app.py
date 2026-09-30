"""
提示词润色助手 - Streamlit 版本
功能：提示词优化、评分、场景模板、多风格输出
运行：streamlit run app.py
"""

import streamlit as st
import json
import re
import time
from datetime import datetime

# ============== 页面配置 ==============
st.set_page_config(
    page_title="提示词润色助手",
    page_icon="✨",
    layout="wide"
)

# ============== 样式 ==============
st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stButton>button { width: 100%; }
    .score-card {
        background: #f0f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .result-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4a90d9;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# ============== 场景模板 ==============
SCENARIOS = {
    "通用模式": {
        "description": "通用提示词优化",
        "keywords": [],
        "template": ""
    },
    "代码开发": {
        "description": "编程、调试、代码审查",
        "keywords": ["代码", "函数", "bug", "调试", "编程", "python", "java", "javascript"],
        "template": "你是一位资深{language}开发专家，请{task}。要求：\n1. 代码规范、注释清晰\n2. 考虑边界条件和异常处理\n3. 给出最优解并说明复杂度"
    },
    "小红书文案": {
        "description": "小红书笔记、标题、标签",
        "keywords": ["小红书", "文案", "种草", "笔记", "标题"],
        "template": "你是一位小红书爆款文案写手，请{task}。要求：\n1. 标题吸引眼球，带emoji\n2. 正文口语化、有共鸣\n3. 结尾加相关话题标签"
    },
    "数据分析": {
        "description": "数据分析、报告、可视化",
        "keywords": ["数据", "分析", "报表", "统计", "可视化"],
        "template": "你是一位数据分析师，请{task}。要求：\n1. 明确分析目标和指标\n2. 给出分析方法和步骤\n3. 输出结论和建议"
    },
    "创意写作": {
        "description": "故事、小说、创意内容",
        "keywords": ["故事", "小说", "创意", "写作", "文案"],
        "template": "你是一位创意写作专家，请{task}。要求：\n1. 情节有吸引力\n2. 人物形象鲜明\n3. 语言生动有画面感"
    },
    "总结提炼": {
        "description": "摘要、总结、会议纪要",
        "keywords": ["总结", "摘要", "提炼", "纪要", "归纳"],
        "template": "你是一位内容提炼专家，请{task}。要求：\n1. 保留核心信息，去除冗余\n2. 分点清晰，逻辑分明\n3. 控制在指定字数内"
    }
}

STYLES = {
    "简洁版": "精简、直接、要点突出",
    "详细版": "完整、细致、步骤清晰",
    "专家版": "专业、深入、术语准确"
}

# ============== 评分系统 ==============
def score_prompt(prompt_text):
    """对提示词进行四维度评分"""
    scores = {}
    
    # 清晰度：是否有明确的任务描述
    clarity = min(100, 20 + len(prompt_text) * 0.3)
    if any(k in prompt_text for k in ["请", "帮我", "你是", "扮演", "角色"]):
        clarity += 20
    scores["清晰度"] = min(100, int(clarity))
    
    # 结构化：是否有分点、编号
    structure = 30
    if re.search(r'\d+[.、)]', prompt_text):
        structure += 30
    if "\n" in prompt_text:
        structure += 20
    if any(k in prompt_text for k in ["要求", "步骤", "格式", "输出"]):
        structure += 20
    scores["结构化程度"] = min(100, structure)
    
    # 约束完整性：是否有约束条件
    constraint = 20
    if any(k in prompt_text for k in ["不要", "避免", "必须", "一定", "只能", "限制"]):
        constraint += 30
    if any(k in prompt_text for k in ["字数", "长度", "格式", "风格", "语气"]):
        constraint += 30
    if len(prompt_text) > 100:
        constraint += 20
    scores["约束完整性"] = min(100, constraint)
    
    # 目标明确度：是否有明确目标
    goal = 30
    if any(k in prompt_text for k in ["目标", "目的", "为了", "用于", "实现"]):
        goal += 30
    if any(k in prompt_text for k in ["输出", "返回", "结果", "格式"]):
        goal += 20
    if prompt_text.endswith(("。", "！", "？", ".")):
        goal += 10
    scores["目标明确度"] = min(100, goal)
    
    return scores

# ============== 规则模板优化 ==============
def rule_based_optimize(prompt_text, style, scenario):
    """基于规则模板的提示词优化"""
    result = []
    
    # 1. 角色设定
    role_map = {
        "通用模式": "你是一位专业的AI助手",
        "代码开发": "你是一位资深全栈开发工程师，精通多种编程语言和最佳实践",
        "小红书文案": "你是一位资深新媒体运营专家，擅长小红书爆款文案创作",
        "数据分析": "你是一位资深数据分析师，擅长从数据中发现洞察",
        "创意写作": "你是一位资深创意写作专家，作品曾获多项文学奖项",
        "总结提炼": "你是一位资深内容编辑，擅长信息提炼和结构化表达"
    }
    result.append(f"【角色设定】\n{role_map.get(scenario, '你是一位专业的AI助手')}")
    
    # 2. 任务描述
    result.append(f"\n【任务描述】\n{prompt_text.strip()}")
    
    # 3. 优化要求
    style_requirements = {
        "简洁版": "输出简洁明了，直击要点，避免冗余表述",
        "详细版": "输出完整详细，包含步骤说明和注意事项",
        "专家版": "输出专业深入，使用行业术语，提供多角度分析"
    }
    result.append(f"\n【输出要求】\n1. {style_requirements.get(style, '输出清晰准确')}")
    result.append("2. 分点作答，逻辑清晰")
    result.append("3. 如有不确定的信息，请明确说明")
    
    # 4. 场景特定要求
    if scenario == "代码开发":
        result.append("4. 代码需包含注释，说明关键逻辑")
        result.append("5. 考虑边界条件和异常处理")
    elif scenario == "小红书文案":
        result.append("4. 标题带emoji，吸引眼球")
        result.append("5. 正文口语化，有代入感")
        result.append("6. 结尾加3-5个相关话题标签")
    elif scenario == "数据分析":
        result.append("4. 明确分析指标和方法")
        result.append("5. 给出数据驱动的结论和建议")
    
    result.append("\n【输出格式】\n按上述要求，直接输出结果，不要额外解释。")
    
    return "\n".join(result)

# ============== 大模型优化 ==============
def llm_optimize(prompt_text, style, scenario, api_key):
    """调用大模型进行优化"""
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = f"""你是一位提示词工程专家，擅长优化AI提示词。
请将用户提供的原始提示词优化为更专业、更有效的版本。

优化要求：
1. 风格：{style}（{STYLES.get(style, '')}）
2. 场景：{scenario}
3. 保留原始意图，不改变核心需求
4. 增加角色设定、约束条件、输出格式
5. 只输出优化后的提示词，不要解释"""
        
        data = {
            "model": "doubao-pro-32k",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API调用失败：{response.status_code} - {response.text}"
            
    except ImportError:
        return "错误：需要安装 requests 库，请运行 pip install requests"
    except Exception as e:
        return f"调用出错：{str(e)}"

# ============== 主界面 ==============
st.title("✨ 提示词润色助手")
st.caption("让你的提示词更专业、更有效")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 设置")
    
    # API Key 配置
    api_key = st.text_input(
        "豆包 API Key",
        type="password",
        help="在火山引擎控制台申请，用于大模型润色模式",
        placeholder="sk-xxxxxxxx"
    )
    
    if api_key:
        st.success("✅ API Key 已配置")
    else:
        st.info("💡 不填API Key可使用规则模板模式")
    
    st.divider()
    
    # 历史记录
    st.subheader("📝 历史记录")
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"{item['time']} - {item['scenario']}"):
                st.text("原文：" + item["original"][:50] + "...")
                st.text("风格：" + item["style"])
    else:
        st.caption("暂无历史记录")

# 主区域
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 原始提示词")
    
    # 场景选择
    scenario = st.selectbox(
        "选择场景",
        options=list(SCENARIOS.keys()),
        help="选择后会自动匹配该场景的优化策略"
    )
    st.caption(SCENARIOS[scenario]["description"])
    
    # 风格选择
    style = st.radio(
        "输出风格",
        options=list(STYLES.keys()),
        horizontal=True
    )
    
    # 输入框
    prompt_input = st.text_area(
        "输入你的提示词",
        height=200,
        placeholder="例如：帮我写一个Python排序算法"
    )
    
    # 模式选择
    mode = st.radio(
        "优化模式",
        options=["规则模板", "大模型润色"],
        horizontal=True
    )
    
    if mode == "大模型润色" and not api_key:
        st.warning("⚠️ 请先在左侧填写 API Key")
    
    # 优化按钮
    if st.button("🚀 开始优化", type="primary", use_container_width=True):
        if not prompt_input.strip():
            st.error("请输入提示词")
        elif mode == "大模型润色" and not api_key:
            st.error("大模型模式需要配置 API Key")
        else:
            with st.spinner("正在优化中..."):
                # 评分
                original_scores = score_prompt(prompt_input)
                
                # 优化
                if mode == "规则模板":
                    optimized = rule_based_optimize(prompt_input, style, scenario)
                    time.sleep(0.5)  # 模拟处理时间
                else:
                    optimized = llm_optimize(prompt_input, style, scenario, api_key)
                
                optimized_scores = score_prompt(optimized)
                
                # 保存到历史
                st.session_state.history.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "original": prompt_input,
                    "optimized": optimized,
                    "scenario": scenario,
                    "style": style,
                    "mode": mode
                })
                
                # 保存结果到 session
                st.session_state.result = {
                    "original": prompt_input,
                    "optimized": optimized,
                    "original_scores": original_scores,
                    "optimized_scores": optimized_scores
                }

with col2:
    st.subheader("✨ 优化结果")
    
    if "result" in st.session_state:
        result = st.session_state.result
        
        # 评分对比
        st.markdown("### 📊 评分对比")
        score_cols = st.columns(4)
        dimensions = ["清晰度", "结构化程度", "约束完整性", "目标明确度"]
        
        for i, dim in enumerate(dimensions):
            with score_cols[i]:
                orig = result["original_scores"][dim]
                opt = result["optimized_scores"][dim]
                delta = opt - orig
                delta_color = "🟢" if delta > 0 else "🔴" if delta < 0 else "⚪"
                st.metric(
                    dim,
                    f"{opt}分",
                    f"{delta:+d}分 {delta_color}"
                )
        
        st.divider()
        
        # 优化结果
        st.markdown("### 📄 优化后提示词")
        st.markdown(f'<div class="result-box">{result["optimized"]}</div>', unsafe_allow_html=True)
        
        # 复制按钮
        st.code(result["optimized"], language="text")
        
        # 操作按钮
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📋 复制结果", use_container_width=True):
                st.toast("已复制到剪贴板！")
        with btn_col2:
            if st.button("🔄 重新优化", use_container_width=True):
                st.rerun()
        
    else:
        st.info("👈 在左侧输入提示词，点击「开始优化」")

# 底部说明
st.divider()
st.caption("""
💡 使用技巧：
1. 选择合适的场景可以获得更精准的优化
2. 大模型润色效果更好，但需要 API Key
3. 规则模板完全离线可用，适合简单场景
4. 优化后记得复制结果到你的AI工具中使用
""")
#（注：内容由AI生成）
