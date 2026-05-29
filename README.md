# Taobao CTR Dashboard

An interactive Streamlit dashboard for exploring advertisement click-through-rate
features and model comparison results. The project was built as a course design
demo and cleaned for public portfolio use.

## Features

- Overview of advertisement, user, and click behavior features
- Hourly CTR trend analysis
- Model comparison page for CTR prediction experiments
- Feature and audience profiling pages
- Small sample data for running the dashboard locally

## Tech Stack

- Python
- Streamlit
- Pandas and NumPy
- Plotly, Matplotlib, and Seaborn

## Project Structure

```text
app.py                 # Streamlit entry point
pages/                 # Streamlit multi-page dashboard
utils/data_loader.py   # CSV loading helper
data/raw/              # Small anonymized sample used by the demo
data/processed/        # Aggregated analysis outputs
```

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Data and Compliance Notes

The original raw course dataset is not included. This repository only contains a
small sample and aggregated CSV outputs so the dashboard can be demonstrated.
Do not use this repository as a source of the complete dataset. To reproduce the
full experiment, obtain the dataset from its original authorized source and place
it under `data/raw/`.

## Status

Portfolio-ready course project demo.
