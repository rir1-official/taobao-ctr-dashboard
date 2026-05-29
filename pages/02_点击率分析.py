import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import DataLoader

st.set_page_config(page_title="CTR 核心分析", page_icon="📈", layout="wide")
st.title("📈 点击率 (CTR) 核心指标分析")

# 1. 加载数据 (user_ad_data.csv)
with st.spinner("正在计算全量数据指标..."):
    df = DataLoader.load_data('user_ad_data.csv', source='raw')

if df is None or df.empty:
    st.error("请检查 data/raw/user_ad_data.csv 是否存在！")
    st.stop()

# 2. 数据清洗
df.columns = df.columns.str.strip()  # 去除列名空格
if 'clk' not in df.columns or 'hour' not in df.columns:
    st.error(f"关键列缺失！当前列名: {list(df.columns)}，需要: clk, hour")
    st.stop()

# 3. 聚合计算
# clk=1代表点击，clk=0代表未点击。总数是曝光，sum是点击
df_hourly = df.groupby('hour')['clk'].agg(['count', 'sum']).reset_index()
df_hourly.columns = ['hour', 'pv', 'click']
df_hourly['ctr'] = (df_hourly['click'] / df_hourly['pv'] * 100).round(2)

# 4. 顶部 KPI
st.subheader("1. 关键业务指标")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_pv = df_hourly['pv'].sum()
total_click = df_hourly['click'].sum()
avg_ctr = (total_click / total_pv * 100)

kpi1.metric("总曝光量 (PV)", f"{total_pv:,.0f}")
kpi2.metric("总点击量 (Click)", f"{total_click:,.0f}")
kpi3.metric("平均 CTR", f"{avg_ctr:.2f}%")
kpi4.metric("数据时段", "0点 - 23点")

st.divider()

# 5. 图表展示
st.subheader("2. CTR 时间趋势分析")
col1, col2 = st.columns([2, 1])

with col1:
    fig_line = px.line(df_hourly, x='hour', y='ctr', markers=True,
                       title='24小时点击率变化趋势',
                       labels={'ctr': '点击率(%)', 'hour': '小时'})
    fig_line.add_hline(y=avg_ctr, line_dash="dash", line_color="red", annotation_text="平均线")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_hourly['hour'], y=df_hourly['pv'], name='曝光', marker_color='#AABBCC'))
    fig_bar.add_trace(go.Scatter(x=df_hourly['hour'], y=df_hourly['click'], name='点击', yaxis='y2', line=dict(color='orange')))
    fig_bar.update_layout(title='曝光 vs 点击', yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. 漏斗图 (基于真实数据估算)
st.subheader("3. 转化漏斗 (Funnel)")
funnel_data = dict(
    number=[total_pv, total_pv*0.6, total_click, total_click*0.2],
    stage=["曝光", "浏览", "点击", "购买(估算)"]
)
fig_funnel = px.funnel(funnel_data, x='number', y='stage', title='全链路转化漏斗')
st.plotly_chart(fig_funnel, use_container_width=True)