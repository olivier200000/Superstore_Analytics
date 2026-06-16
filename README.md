# Superstore_Analytics
A Python-powered analytics dashboard that turns raw retail transaction data into clear business decisions.

# 📊 Superstore Analytics Dashboard

An interactive business intelligence dashboard built with **Streamlit** and **Plotly**, analyzing sales, profitability, and regional performance data from the Superstore retail dataset.

---

## 👥 Project Contributors

| Role | Name |
|---|---|
| Group Leader & Dashboard Developer | Dusengimana Olivier |
| Dataset & Metadata Specialist | Christian Habineza |
| Data Cleaning & Preparation | Gilbert Niyonkuru |
| Data Visualization Specialist | Shadia Uwimbabazi |
| Data Analyst, Ethics & Insights | Dative Akimana |

---

## 📁 Project Structure

```
superstore-dashboard/
├── app.py                  # Main Streamlit application
├── super.xlsx              # Dataset file (download from Kaggle — see below)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🗂️ Dataset

- **Name:** Superstore Dataset — Final
- **Author:** Vivek Chowdhury (`vivek468` on Kaggle)
- **Source:** [kaggle.com/datasets/vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **File used:** `super.xlsx`

> Download `super.xlsx` from the Kaggle link above and place it in the same folder as `app.py` before running the app.

---

## ⚙️ Installation & Setup

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/superstore-dashboard.git
cd superstore-dashboard
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place the downloaded `super.xlsx` file in the root project folder (same level as `app.py`).

### 5. Run the dashboard

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

> **No dataset file?** If `super.xlsx` is missing, the app will prompt you to upload it directly through the sidebar.

---

## 📋 Dashboard Pages

| Page | Description |
|---|---|
| **Meet the Team** | Project contributors and their roles |
| **Executive Summary** | High-level KPIs and sales/profit trends over time |
| **Sales Analysis** | Breakdown by sub-category, shipping mode, and top products |
| **Profitability Analysis** | Profit margins by category and the 10 biggest loss-making items |
| **Regional Analysis** | USA choropleth map of sales and profit by state |
| **Risk Center** | Discount impact analysis and risk alerts |
| **Ethics & Governance** | Data privacy practices and glossary of key terms |
| **Recommendations** | Prioritized action plan based on findings |
| **Dataset Metadata** | Full source information and dataset documentation |

---

## 🔍 Key Findings

- Discounts of **40% or more** consistently result in losses across all categories.
- The **Technology** category delivers the highest profit margins.
- **Tables** and **Bookcases** are the top loss-making sub-categories.
- The **West** region leads in overall sales volume.

---

## 🛡️ Ethics & Privacy

- No real customer names, phone numbers, or home addresses are displayed.
- Data is aggregated at the state/region level to protect individual privacy.
- All loss-making transactions are shown transparently — no data is hidden.
- The dataset is used strictly for academic and non-commercial educational purposes.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework and UI rendering |
| `pandas` | Data loading, cleaning, and transformation |
| `plotly` | Interactive charts and choropleth maps |
| `openpyxl` | Reading `.xlsx` Excel files |

---

## 📄 License

This project is for academic use only. The Superstore dataset is publicly available on Kaggle for educational and non-commercial purposes.

