import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="模型对比", page_icon="🤖", layout="wide")
st.title("🤖 算法模型性能竞技场")

# 侧边栏
st.sidebar.header("⚙️ 模型配置")
selected_models = st.sidebar.multiselect(
    "选择对比模型",
    ['LR', 'GBDT', 'XGBoost', 'DeepFM', 'DIN'],
    default=['LR', 'XGBoost', 'DeepFM']
)

# 1. 模拟数据 (这里使用静态数据展示，代表后台训练好的结果)
data = {
    'Model': ['LR', 'GBDT', 'XGBoost', 'DeepFM', 'DIN'],
    'AUC': [0.72, 0.78, 0.81, 0.86, 0.88],
    'LogLoss': [0.55, 0.48, 0.42, 0.35, 0.33],
    'F1-Score': [0.65, 0.70, 0.74, 0.79, 0.81],
    'Inference_Time_ms': [5, 12, 15, 35, 42]
}
df_models = pd.DataFrame(data)
df_display = df_models[df_models['Model'].isin(selected_models)]

# 2. 核心指标对比
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 AUC (越高越好)")
    fig_auc = px.bar(df_display, x='Model', y='AUC', color='AUC',
                     range_y=[0.6, 1.0], title="各模型 AUC 评分", text_auto=True)
    st.plotly_chart(fig_auc, use_container_width=True)

with col2:
    st.subheader("📋 详细数据表")
    st.dataframe(df_display, use_container_width=True)

# 3. 雷达图
st.divider()
st.subheader("🕸️ 多维能力雷达图")

fig_radar = go.Figure()
categories = ['AUC', 'F1-Score', '1-LogLoss', 'Speed']

for i, row in df_display.iterrows():
    # 简单的归一化处理用于绘图
    values = [
        row['AUC'],
        row['F1-Score'],
        1 - row['LogLoss'],
        1 - (row['Inference_Time_ms'] / 100)
    ]
    fig_radar.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name=row['Model']))

fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
st.plotly_chart(fig_radar, use_container_width=True)

# -----------------------------------------------------------------------------
# [修改部分] 4. 智能动态结论
# -----------------------------------------------------------------------------
if not df_display.empty:
    # 1. 找出各项指标的最优模型
    best_auc_row = df_display.loc[df_display['AUC'].idxmax()]
    fastest_row = df_display.loc[df_display['Inference_Time_ms'].idxmin()]

    best_model = best_auc_row['Model']
    fastest_model = fastest_row['Model']

    # 2. 构建动态文案
    insight_text = "### 💡 智能诊断报告\n\n"

    # 分析精度
    insight_text += f"**🏆 精度冠军**：**{best_model}** (AUC: {best_auc_row['AUC']})\n"
    if best_model in ['DeepFM', 'DIN']:
        insight_text += "> *深度学习模型在捕捉复杂特征交叉方面表现出色，预测准确度最高。*\n\n"
    else:
        insight_text += "> *在当前选中的模型组中，该模型预测能力最强。*\n\n"

    # 分析速度
    insight_text += f"**⚡ 速度之星**：**{fastest_model}** (耗时: {fastest_row['Inference_Time_ms']}ms)\n"
    if fastest_model == 'LR':
        insight_text += "> *线性模型虽然简单，但推理速度极快，适合高并发场景。*\n\n"
    else:
        insight_text += "> *在保持一定精度的同时，该模型拥有最快的响应速度。*\n\n"

    # 综合建议
    insight_text += "**🚀 上线建议**：\n"
    if best_model == fastest_model:
        insight_text += f"无需纠结！**{best_model}** 在精度和速度上均表现最优，是完美的上线选择。"
    else:
        auc_diff = best_auc_row['AUC'] - fastest_row['AUC']
        insight_text += f"- 若业务**以转化为核心目标**，强烈推荐 **{best_model}**，相比最快模型 AUC 提升了 **+{auc_diff:.2f}**。\n"
        insight_text += f"- 若线上**服务器压力大或对延迟极度敏感**（如实时竞价），可以考虑 **{fastest_model}** 作为备选方案。"

    st.info(insight_text)
else:
    st.warning("请在左侧侧边栏至少选择一个模型进行对比。")