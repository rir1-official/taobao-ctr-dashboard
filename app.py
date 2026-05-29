import streamlit as st
import platform
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. 全局配置
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="淘宝广告CTR预估系统",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. 字体配置 (解决 Linux/Windows 中文乱码)
# -----------------------------------------------------------------------------
system_name = platform.system()
if system_name == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif system_name == "Darwin":  # Mac
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------------------------------------------------------
# 3. 侧边栏
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.alicdn.com/tfs/TB1_uT8a5ZX8KJjSgjSXXa1qVXa-52-52.png", width=50)
    st.title("CTR 预估系统")
    st.info(
        """
        **项目版本**: v2.0 Pro
        **数据源**: 阿里妈妈搜索广告数据集
        **核心技术**: Spark + Streamlit + XGBoost
        """
    )
    st.divider()
    st.success("✅ 系统状态：在线")

# -----------------------------------------------------------------------------
# 4. 主页内容
# -----------------------------------------------------------------------------
st.title("🛒 淘宝展示广告点击率预估系统")

st.markdown("""
### 👋 欢迎使用
本系统基于海量用户行为日志，提供全链路的广告点击率（CTR）分析与预测能力。

#### 🚀 核心功能模块：
1.  **📊 数据概览**: 实时查看 `user_ad_data` 等核心数据集的分布与质量。
2.  **📈 CTR 核心分析**: 基于真实点击日志 (`clk`) 计算 24 小时点击率趋势。
3.  **🤖 模型对比**: 算法大比拼，直观展示模型间的性能差异。
4.  **🔍 深度特征挖掘**: 挖掘 **价格**、**品类** 与点击率的非线性关系。
5.  **🎯 用户画像透视**: 基于 `final_gender_code` 等字段进行多维用户分群。

#### 💡 快速开始
👈 请点击左侧侧边栏的 **Pages** 菜单开始探索！
""")

# 模拟的实时看板
col1, col2, col3, col4 = st.columns(4)
col1.metric("今日处理数据", "114万+", "user_ad_data")
col2.metric("当前最佳模型", "DeepFM", "AUC 0.86")
col3.metric("实时 CTR", "4.82%", "+0.12%")
col4.metric("覆盖用户数", "5000+", "user_data")

st.divider()
st.caption("Course project demo | Powered by Streamlit")
