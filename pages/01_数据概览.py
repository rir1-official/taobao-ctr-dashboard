import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import DataLoader

# -----------------------------------------------------------------------------
# 0. 核心配置与字典
# -----------------------------------------------------------------------------
st.set_page_config(page_title="数据概览", page_icon="📊", layout="wide")

# 字段中文翻译映射
COLUMN_MEANINGS = {
    'final_gender_code': '用户性别',
    'age_level': '年龄层次',
    'pvalue_level': '消费档次',
    'shopping_level': '购物深度',
    'new_user_class_level': '城市层级',
    'price': '商品价格',
    'cate_id': '品类ID',
    'hour': '小时',
    'clk': '点击行为'
}


# -----------------------------------------------------------------------------
# 1. 数据加载逻辑 (自动执行)
# -----------------------------------------------------------------------------
@st.cache_data
def load_dataset(limit):
    """
    封装加载逻辑，默认加载 user_ad_data.csv
    """
    # 默认加载最全的 user_ad_data.csv
    file_name = "user_ad_data.csv"
    df = DataLoader.load_data(file_name, source='raw')

    if df is not None and not df.empty:
        # 截取采样数据
        df_display = df.head(limit).copy()
        df_display.columns = df_display.columns.str.strip()  # 去空格
        return df_display
    return None


# -----------------------------------------------------------------------------
# 2. 侧边栏配置 (仅保留性能控制)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 数据配置")
    # 既然默认加载，只留一个采样控制即可，调整后自动刷新
    load_limit = st.slider("数据采样行数 (影响加载速度)", 1000, 50000, 10000, step=1000)
    st.caption("💡 说明：为了演示流畅性，默认只加载部分数据。调整滑块可实时更新样本量。")

# -----------------------------------------------------------------------------
# 3. 核心页面渲染
# -----------------------------------------------------------------------------
# 直接调用加载函数
df = load_dataset(load_limit)

if df is not None:
    st.title("📊 数据集全貌概览")
    st.success(f"✅ 数据已自动加载 | 当前样本量: {len(df)} 行")

    # =========================================================================
    # 第一部分：6大核心特征直观展示 (固定布局)
    # =========================================================================
    st.markdown("### 1️⃣ 核心特征分布 (Six Key Features)")
    st.markdown("以下为数据集最关键的 6 个维度分布情况：")

    # 定义我们要画的6个图: (列名, 标题, 图表类型, 简要说明)
    chart_configs = [
        ('final_gender_code', '用户性别分布', 'pie',
         '👥 **说明**: 展示了平台用户的性别构成比例。'),

        ('pvalue_level', '消费档次分布', 'bar',
         '💰 **说明**: 1=低档，2=中档，3=高档。反映了用户群体的购买力水平和消费层级。'),

        ('shopping_level', '购物深度分布', 'bar',
         '🛍️ **说明**: 1=浅层用户，2=中度用户，3=深度用户。展示用户使用淘宝的依赖程度。'),

        ('age_level', '年龄层次分布', 'bar',
         '🎂 **说明**: 数值越大代表年龄越大。展示了广告受众的年龄结构分布。'),

        ('new_user_class_level', '城市层级分布', 'bar',
         '🏙️ **说明**: 1-4 代表不同级别的城市（一线到四线）。分析用户主要来自哪些地域市场。'),

        ('price', '广告价格分布', 'hist',
         '🏷️ **说明**: 商品价格分布直方图。**已自动去除前1%的极值**，以展示核心价格区间。')
    ]

    # 创建 2行3列 的布局
    row1 = st.columns(3)
    row2 = st.columns(3)
    all_slots = row1 + row2

    # 循环画图
    for i, (col, title, chart_type, desc) in enumerate(chart_configs):
        if i < 6:
            with all_slots[i]:
                if col in df.columns:
                    try:
                        # --- 画图逻辑 ---
                        if chart_type == 'hist':  # 价格分布
                            p99 = df[col].quantile(0.99)
                            clean_data = df[df[col] <= p99]
                            fig = px.histogram(clean_data, x=col, title=f"{title} (去极值)",
                                               color_discrete_sequence=['#0068C9'], nbins=30)
                            fig.update_layout(height=300)  # 控制高度

                        elif chart_type == 'pie':  # 饼图
                            counts = df[col].value_counts().reset_index()
                            counts.columns = [col, 'count']
                            if col == 'final_gender_code':
                                counts[col] = counts[col].map({1: '男', 2: '女'}).fillna('未知')
                            fig = px.pie(counts, values='count', names=col, title=title, hole=0.4)
                            fig.update_layout(height=300)

                        else:  # 柱状图
                            counts = df[col].value_counts().sort_index().reset_index()
                            counts.columns = [col, 'count']
                            counts[col] = counts[col].astype(str)
                            fig = px.bar(counts, x=col, y='count', title=title,
                                         text='count', color='count', color_continuous_scale='Blues')
                            fig.update_layout(height=300)

                        st.plotly_chart(fig, use_container_width=True)
                        # --- 在这里增加简要说明 ---
                        st.caption(desc)

                    except Exception as e:
                        st.warning(f"{title} 渲染失败: {e}")
                else:
                    st.info(f"⚠️ 暂无 {col} 数据")

    st.divider()

    # =========================================================================
    # 第二部分：智能探索模块
    # =========================================================================
    st.markdown("### 2️⃣ 智能多维探索 (Intelligent Exploration)")

    with st.expander("🎨 点击展开/折叠智能探索面板", expanded=True):
        col_tool1, col_tool2 = st.columns([1, 3])

        with col_tool1:
            st.info("💡 **自由分析模式**：\n此处可选择任意列进行深度分析，支持去极值操作。")
            all_cols = df.columns.tolist()
            target_col = st.selectbox("👉 选择要分析的列", all_cols)
            meaning = COLUMN_MEANINGS.get(target_col, "暂无说明")
            st.caption(f"含义: {meaning}")

        with col_tool2:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

            if target_col in numeric_cols and len(df[target_col].unique()) > 10:
                remove_outlier = st.checkbox("去除 1% 极值", value=True, key='smart_remove')
                plot_data = df
                if remove_outlier:
                    limit = df[target_col].quantile(0.99)
                    plot_data = df[df[target_col] <= limit]

                fig_smart = px.histogram(plot_data, x=target_col, nbins=50, title=f"{target_col} 分布详情",
                                         marginal="box")
                st.plotly_chart(fig_smart, use_container_width=True)
            else:
                counts = df[target_col].value_counts().head(20).reset_index()
                counts.columns = [target_col, 'count']
                counts[target_col] = counts[target_col].astype(str)
                fig_smart = px.bar(counts, x=target_col, y='count', title=f"{target_col} Top 20 分布", color='count')
                st.plotly_chart(fig_smart, use_container_width=True)

else:
    st.error("❌ 数据加载失败，请检查 utils/data_loader.py 或数据文件是否存在。")