import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import DataLoader

# -----------------------------------------------------------------------------
# 1. 页面配置与字典映射
# -----------------------------------------------------------------------------
st.set_page_config(page_title="用户画像与效果", page_icon="🎯", layout="wide")

# 字典映射 (让数据说人话)
GENDER_MAP = {1: '男', 2: '女', 0: '未知'}
LEVEL_MAP = {1: '低档', 2: '中档', 3: '高档'}
SHOPPING_MAP = {1: '浅层', 2: '中度', 3: '深度'}
CITY_MAP = {1: '一线', 2: '二线', 3: '三线', 4: '四线+'}
OCCUPATION_MAP = {0: '非大学生', 1: '大学生'}

st.title("🎯 广告受众画像与效果深度洞察")


# -----------------------------------------------------------------------------
# 2. 数据加载
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 我们只需要 user_ad_data，因为它包含了 用户信息 + 广告ID + 点击行为
    df = DataLoader.load_data('user_ad_data.csv', source='raw')
    if df is not None:
        df.columns = df.columns.str.strip()

        # 预处理：映射字段，生成用于画图的中文列
        if 'final_gender_code' in df.columns:
            df['性别'] = df['final_gender_code'].map(GENDER_MAP).fillna('未知')
        if 'pvalue_level' in df.columns:
            df['消费档次'] = df['pvalue_level'].map(LEVEL_MAP).fillna('未知')
        if 'shopping_level' in df.columns:
            df['购物深度'] = df['shopping_level'].map(SHOPPING_MAP).fillna('未知')
        if 'new_user_class_level' in df.columns:
            df['城市层级'] = df['new_user_class_level'].map(CITY_MAP).fillna('未知')
        if 'occupation' in df.columns:
            df['身份'] = df['occupation'].map(OCCUPATION_MAP).fillna('未知')
        if 'age_level' in df.columns:
            df['年龄层次'] = df['age_level'].apply(lambda x: f"Level {x}")
        if 'cms_segid' in df.columns:
            df['微群ID'] = df['cms_segid'].apply(lambda x: f"微群{x}")
        if 'cms_group_id' in df.columns:
            df['群体ID'] = df['cms_group_id'].apply(lambda x: f"群体{x}")

    return df


df = load_data()

# -----------------------------------------------------------------------------
# 3. 页面逻辑
# -----------------------------------------------------------------------------
if df is not None and not df.empty:

    # 定义两个标签页
    tab1, tab2 = st.tabs(["👑 爆款广告受众深挖 (Top Ad)", "🏆 广告效果排行榜"])

    # =========================================================================
    # Tab 1: 爆款广告受众深挖
    # =========================================================================
    with tab1:
        st.subheader("🔥 点击量 Top 1 广告深度画像")

        # 1. 自动计算点击量最高的广告ID
        clicked_df = df[df['clk'] == 1]

        if not clicked_df.empty:
            ad_clicks = clicked_df['adgroup_id'].value_counts()
            top_ad_id = ad_clicks.idxmax()
            top_ad_count = ad_clicks.max()

            # 允许用户切换
            col_sel1, col_sel2 = st.columns([1, 3])
            with col_sel1:
                top_10_ids = ad_clicks.head(10).index.tolist()
                target_ad = st.selectbox("选择广告ID (默认显示点击王)", top_10_ids, index=0)

            with col_sel2:
                if target_ad == top_ad_id:
                    st.success(f"👑 **当前展示的是点击冠军：ID {target_ad}** (点击量: {top_ad_count})")
                else:
                    st.info(f"正在分析广告：{target_ad}")

            # 2. 筛选目标数据
            target_users = df[(df['adgroup_id'] == target_ad) & (df['clk'] == 1)]

            if not target_users.empty:
                st.divider()
                st.markdown(f"#### 📊 广告 ID 【{target_ad}】 的点击用户特征分布")

                dimensions = [
                    ('微群ID', '微群分布'),
                    ('群体ID', '群体分布'),
                    ('性别', '性别分布'),
                    ('年龄层次', '年龄分布'),
                    ('购物深度', '购物深度'),
                    ('身份', '用户身份'),
                    ('城市层级', '城市层级'),
                    ('消费档次', '消费档次')
                ]

                row1 = st.columns(4)
                row2 = st.columns(4)
                all_cols = row1 + row2

                summary_dict = {}

                for i, (col, title) in enumerate(dimensions):
                    with all_cols[i]:
                        if col in target_users.columns:
                            counts = target_users[col].value_counts().reset_index()
                            counts.columns = [col, '人数']
                            top_val = counts.iloc[0][col]
                            summary_dict[title] = top_val

                            fig = px.pie(counts, values='人数', names=col, title=title, hole=0.5)
                            fig.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0), height=200)
                            fig.update_traces(textposition='inside', textinfo='percent+label')
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.caption(f"暂无 {title} 数据")

                st.info(f"""
                💡 **分析结论 (自动生成)**：
                分析可得，观看该广告({target_ad})最多的人群来源于 **{summary_dict.get('微群分布', '未知')}**。
                其中 **{summary_dict.get('性别分布', '未知')}** 性略多。
                绝大多数是 **{summary_dict.get('年龄分布', '未知')}** 的人。
                他们大多数购物深度为 **{summary_dict.get('购物深度', '未知')}**。
                """)
            else:
                st.warning("该广告暂无点击数据。")
        else:
            st.warning("数据集中暂无点击行为。")

    # =========================================================================
    # Tab 2: 广告效果排行榜
    # =========================================================================
    with tab2:
        st.subheader("🏆 广告点击量排行榜")

        # 1. 数据聚合
        ad_stats = df.groupby('adgroup_id').agg(
            展示量=('clk', 'count'),
            点击量=('clk', 'sum')
        ).reset_index()

        # 2. 筛选 Top 10
        valid_ads = ad_stats[ad_stats['展示量'] > 10].copy()
        top_10_clicks = valid_ads.sort_values('点击量', ascending=False).head(10)

        # 3. 【关键排序】：按 ID 从大到小排序 (左边大，右边小)
        top_10_clicks = top_10_clicks.sort_values('adgroup_id', ascending=False)

        # 4. 【关键处理】：转成字符串，确保不按数值分布X轴，而是按类别紧密排列
        top_10_clicks['adgroup_id'] = top_10_clicks['adgroup_id'].astype(str)

        # 5. 画图
        fig_click = px.bar(
            top_10_clicks,
            x='adgroup_id',
            y='点击量',
            text='点击量',  # 柱子上显示数字
            title="Top 10 广告点击分布 (按ID降序)",
            color='点击量',
            color_continuous_scale='Blues'  # 蓝色渐变看起来比较像直方图风格
        )

        # 6. 样式定制
        fig_click.update_layout(
            # X轴设置：显示标签，标题设为None(如果不需要 "adgroup_id" 字样)
            xaxis=dict(
                title=None,
                showticklabels=True,  # 确保下方显示广告ID
                type='category'       # 显式指定为分类轴，不按数值分布
            ),
            # Y轴设置：隐藏轴线和数字，只看柱子高度
            yaxis=dict(
                visible=False,
                showgrid=False
            ),
            showlegend=False,
            coloraxis_showscale=False, # 隐藏颜色条
            bargap=0.2                 # 间距小一点，让柱子粗一点
        )

        # 7. 柱子加粗与数字显示
        fig_click.update_traces(
            textposition='outside',  # 数字显示在上方
            width=0.7                # 柱子宽度 (0-1)，设置得比较大以显得“粗”
        )

        st.plotly_chart(fig_click, use_container_width=True)

        st.markdown("#### 📋 详细数据表")
        st.dataframe(top_10_clicks)

else:
    st.error("数据加载失败，请检查数据文件。")