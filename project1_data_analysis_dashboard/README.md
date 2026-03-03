# 📊 Data Analysis & Dashboard

A Python-based data analysis pipeline that cleans, analyses, and visualises
sales data — replicating the kind of work typically done in **Power BI** with
Power Query + DAX, all in pure Python.

---

## 🗂️ Project Structure

```
project1_data_analysis_dashboard/
│
├── data/
│   ├── sales_data.csv        ← Raw input dataset
│   └── cleaned_data.csv      ← Auto-generated after running data_cleaning.py
│
├── outputs/
│   └── dashboard.png         ← Auto-generated dashboard image
│
├── data_cleaning.py          ← Step 1 : clean & transform raw data
├── analysis.py               ← Step 2 : run KPI queries & print report
├── dashboard.py              ← Step 3 : generate visual dashboard (PNG)
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone / download the repository
```bash
git clone https://github.com/<your-username>/data-analysis-dashboard.git
cd data-analysis-dashboard
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the pipeline — in order

```bash
# Step 1 — clean the raw data
python data_cleaning.py

# Step 2 — print the analytical report
python analysis.py

# Step 3 — generate the dashboard image
python dashboard.py
```

After Step 3, open **`outputs/dashboard.png`** to see your dashboard.

---

## 📈 What Each Script Does

| Script | Description |
|---|---|
| `data_cleaning.py` | Removes duplicates, parses dates, adds Month / Quarter / Year columns, computes Revenue & Profit Margin KPIs |
| `analysis.py` | Prints KPI summary, top products, revenue by category, regional performance, and monthly trend |
| `dashboard.py` | Renders a dark-themed multi-panel PNG dashboard with KPI cards, bar charts, a pie chart, and a trend line |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Pandas** — data cleaning & aggregation
- **Matplotlib** — dashboard visualisation

---

## 📸 Dashboard Preview

> Run `python dashboard.py` — the output is saved at `outputs/dashboard.png`.

---

## 👤 Author

**Kalikini Chakradhar**  
B.E. Computer Science & Engineering (AI) — Parul University  
[GitHub](https://github.com/Chakri-kalikini)
