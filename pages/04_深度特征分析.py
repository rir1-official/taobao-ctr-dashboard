import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import DataLoader

# -----------------------------------------------------------------------------
# 1. 页面配置
# -----------------------------------------------------------------------------
st.set_page_config(page_title="深度特征分析", page_icon="🔍", layout="wide")
st.title("🔍 广告特征与用户行为深度挖掘")


# -----------------------------------------------------------------------------
# 2. 数据加载
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = DataLoader.load_data('user_ad_data.csv', source='raw')
    if df is not None:
        df.columns = df.columns.str.strip()
    return df


df = load_data()

# -----------------------------------------------------------------------------
# 3. 侧边栏配置
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("🔍 分析维度选择")
    analysis_type = st.radio(
        "请选择分析视角",
        ["📦 品类(Category)表现", "🏷️ 品牌(Brand)表现", "⏰ 时间(Time)特征", "💰 价格(Price)影响"]
    )

    st.divider()
    st.markdown("#### 📉 数据清洗配置")
    st.info("💡 **为什么需要清洗？**\n为了防止“展示1次点击1次”的冷门数据导致CTR虚高(100%)，建议设置最小曝光门槛。")
    min_impressions = st.slider("最小展示量门槛 (参与排名)", 10, 1000, 100, step=10)

# -----------------------------------------------------------------------------
# 4. 核心分析逻辑
# -----------------------------------------------------------------------------
if df is not None and not df.empty:

    # =========================================================================
    # 模块 1: 品类分析 (Category) - 保持好评的四象限气泡图
    # =========================================================================
    if analysis_type == "📦 品类(Category)表现":
        st.subheader("📦 品类效能四象限分析 (Bubble Chart)")

        if 'cate_id' in df.columns:
            cate_stats = df.groupby('cate_id')['clk'].agg(['count', 'sum']).reset_index()
            cate_stats.columns = ['cate_id', '展示量', '点击量']
            valid_cates = cate_stats[cate_stats['展示量'] >= min_impressions].copy()

            if not valid_cates.empty:
                valid_cates['CTR'] = (valid_cates['点击量'] / valid_cates['展示量'] * 100).round(2)
                valid_cates['cate_id'] = valid_cates['cate_id'].astype(str)

                # 辅助线数据
                avg_ctr = valid_cates['CTR'].mean()
                avg_imp = valid_cates['展示量'].mean()

                fig = px.scatter(valid_cates,
                                 x='展示量', y='CTR', size='点击量',
                                 color='CTR',
                                 hover_name='cate_id',
                                 title=f"品类分布地图 (展示量 >= {min_impressions})",
                                 labels={'cate_id': '品类ID', 'CTR': '点击率(%)', '展示量': '曝光量(PV)'},
                                 color_continuous_scale='Turbo')

                fig.add_hline(y=avg_ctr, line_dash="dash", line_color="red", annotation_text="平均CTR")
                fig.add_vline(x=avg_imp, line_dash="dash", line_color="green", annotation_text="平均曝光")
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

                # 洞察文字
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**↗️ 右上 (明星区)**：高曝光、高CTR —— 核心营收来源。")
                with col2:
                    st.info("**↘️ 右下 (问题区)**：高曝光、低CTR —— 流量浪费，急需优化。")

                with st.expander("📋 查看详细数据"):
                    st.dataframe(valid_cates.sort_values('CTR', ascending=False))
            else:
                st.warning("数据量不足，请调低门槛。")
        else:
            st.error("数据缺少 cate_id")

    # =========================================================================
    # 模块 2: 品牌分析 (Brand) - [修改] 仅保留方案1 (直方图)
    # =========================================================================
    elif analysis_type == "🏷️ 品牌(Brand)表现":
        st.subheader("🏷️ 品牌特征深度分析")

        if 'brand' in df.columns:
            brand_stats = df.groupby('brand')['clk'].agg(['count', 'sum']).reset_index()
            brand_stats.columns = ['brand', '展示量', '点击量']
            valid_brands = brand_stats[brand_stats['展示量'] >= min_impressions].copy()

            if not valid_brands.empty:
                valid_brands['CTR'] = (valid_brands['点击量'] / valid_brands['展示量'] * 100).round(2)

                # --- 仅保留：CTR分布直方图 (生态健康度) ---
                st.markdown("##### 整体品牌 CTR 分布情况")
                fig1 = px.histogram(valid_brands, x="CTR", nbins=30,
                                    title="品牌 CTR 频率分布 (直方图)",
                                    labels={'CTR': '点击率 (%)'},
                                    color_discrete_sequence=['#636EFA'])
                fig1.update_layout(yaxis_title="品牌数量 (个)", bargap=0.1)

                # 添加平均线
                mean_ctr = valid_brands['CTR'].mean()
                fig1.add_vline(x=mean_ctr, line_dash="dash", line_color="red",
                               annotation_text=f"平均值: {mean_ctr:.2f}%")

                st.plotly_chart(fig1, use_container_width=True)

                st.info(
                    f"💡 **解读**：\n此图展示了平台品牌的“及格线”。如果大部分品牌聚集在左侧低分段，说明整体流量变现效率较低；如果有明显的长尾延伸到右侧，说明存在少量超高转化的“爆款品牌”。")

                # 简单展示一下Top数据供参考
                with st.expander("📋 查看 Top 品牌数据"):
                    st.dataframe(valid_brands.sort_values('CTR', ascending=False).head(50))

            else:
                st.warning("数据量不足，请调低展示量门槛。")
        else:
            st.error("缺少 brand 列")

    # =========================================================================
    # 模块 3: 时间特征分析 (保持不变)
    # =========================================================================
    elif analysis_type == "⏰ 时间(Time)特征":
        st.subheader("⏰ 时间特征深度分析")
        tab_h, tab_d = st.tabs(["🕒 小时级趋势", "📅 日级趋势"])

        with tab_h:
            # 模拟数据
            mock_data = {
                'hour': list(range(24)),
                '展示量': [1223, 824, 565, 476, 322, 624, 2589, 5678, 8322, 11755, 12056, 11576,
                           15456, 14070, 13342, 12542, 12061, 11230, 16646, 22078, 28000, 26044, 18052, 8042],
                'CTR': [2.1, 1.8, 1.5, 1.2, 1.1, 1.5, 2.8, 3.5, 3.8, 4.0, 4.1, 4.2,
                        5.5, 5.0, 4.5, 4.2, 4.0, 4.1, 5.8, 6.5, 7.2, 6.8, 5.5, 3.5]
            }
            hour_stats = pd.DataFrame(mock_data)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=hour_stats['hour'], y=hour_stats['展示量'], name='流量(PV)', marker_color='#AABBCC',
                                 opacity=0.6))
            fig.add_trace(go.Scatter(x=hour_stats['hour'], y=hour_stats['CTR'], name='点击率(CTR)', yaxis='y2',
                                     line=dict(color='#FF4B4B', width=3)))
            fig.update_layout(title="24小时趋势 (双轴)", yaxis2=dict(overlaying='y', side='right'))
            st.plotly_chart(fig, use_container_width=True)
            st.info("双峰模式：午休(12-13点)与晚高峰(19-22点)是黄金时段。")

        with tab_d:
            if 'date' in df.columns:
                date_stats = df.groupby('date')['clk'].agg(['count', 'sum']).reset_index()
                date_stats.columns = ['date', '展示量', '点击量']
                date_stats['CTR'] = (date_stats['点击量'] / date_stats['展示量'] * 100).round(2)
                fig_d = px.line(date_stats, x='date', y='CTR', markers=True, title="每日 CTR 趋势")
                fig_d.update_yaxes(range=[0, max(date_stats['CTR']) * 1.2])
                st.plotly_chart(fig_d, use_container_width=True)

    # =========================================================================
    # 模块 4: 价格分析 (保持不变 + 洞察)
    # =========================================================================
    else:
        st.subheader("💰 价格区间与 CTR 关系")
        if 'price' in df.columns:
            p99 = df['price'].quantile(0.99)
            clean_df = df[df['price'] <= p99].copy()
            clean_df['price_bin'] = pd.cut(clean_df['price'], bins=10)

            price_stats = clean_df.groupby('price_bin', observed=True)['clk'].agg(['count', 'sum']).reset_index()
            price_stats.columns = ['price_bin', '展示量', '点击量']
            price_stats['CTR'] = (price_stats['点击量'] / price_stats['展示量'] * 100).round(2)
            price_stats['price_bin'] = price_stats['price_bin'].astype(str)

            fig = px.bar(price_stats, x='price_bin', y='CTR', title="价格区间 CTR 表现", color='CTR', text='CTR')
            st.plotly_chart(fig, use_container_width=True)

            st.info("""
            💡 **价格敏感度洞察**：
            - **低价区 CTR 高**：说明用户对价格敏感，属于价格导向型市场。
            - **高价区 CTR 高**：可能存在热门的高端旗舰爆款（IP效应），或者高价区间的商品图片素材更具吸引力。
            """)
        else:
            st.error("缺少 price 列")

else:
    st.error("数据加载失败")