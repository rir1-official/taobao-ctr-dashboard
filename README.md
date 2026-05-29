# Taobao CTR Dashboard / 淘宝广告点击率分析看板

## English

An interactive Streamlit dashboard for exploring advertisement click-through-rate
features and model comparison results. This project was built as a course design
demo and cleaned for public portfolio use.

### Features

- Advertisement, user, and click behavior overview
- Hourly CTR trend analysis
- Model comparison page for CTR prediction experiments
- Feature analysis and audience profiling pages
- Small sample data for local demonstration

### Tech Stack

- Python
- Streamlit
- Pandas and NumPy
- Plotly, Matplotlib, and Seaborn

### Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Data and Compliance

The full original raw dataset is not included. This repository only keeps a
small sample and several aggregated CSV files so the dashboard can be reviewed
and run locally. To reproduce the full experiment, obtain the dataset from an
authorized source and place it under `data/raw/`.

---

## 中文

这是一个基于 Streamlit 的广告点击率（CTR）分析看板，用于展示广告特征、
用户行为、点击趋势和模型对比结果。项目来源于课程设计，已整理为适合公开展示
的作品集版本。

### 功能

- 广告、用户、点击行为数据概览
- 24 小时 CTR 趋势分析
- CTR 预测实验的模型对比页面
- 广告特征分析和用户画像分析
- 保留小型示例数据，便于本地运行演示

### 技术栈

- Python
- Streamlit
- Pandas / NumPy
- Plotly / Matplotlib / Seaborn

### 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### 数据与合规说明

仓库不包含完整原始课程数据集，只保留了小型示例数据和部分聚合统计结果，
用于演示页面功能。若需要复现实验，请从合法授权来源获取原始数据，并放入
`data/raw/` 目录。
