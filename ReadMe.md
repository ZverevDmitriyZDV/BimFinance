# 🏗️ BIM Finance Analyzer

**From BIM to Financial Insight — bridging architecture and investment through code**

---

## 💡 What is this?

A web-based tool that transforms BIM data (from Revit/IFC/Excel) into **financial analytics for real estate developers, architects, and project managers**.

It analyzes room areas and categories, calculates total cost, ROI, payback period, NPV, and visualizes investment scenarios.

Built for professionals who need quick and intelligent insights from spatial data.

---

## 🎯 Who is it for?

- Real estate developers
- Architects and BIM managers
- Construction financial analysts
- PropTech innovators and AEC startups

---

## ⚙️ Features

✅ Upload BIM data in Excel format  
✅ Classify spaces by category (residential, commercial, storage...)  
✅ Choose investment strategy: **Rent vs. Sale**  
✅ Input assumptions (cost per m², rental price, project duration)  
✅ Automatic financial metrics:
- Total project cost
- ROI / NPV / IRR
- Payback time

✅ Visual dashboards (Plotly)
✅ Ready-to-export reports (Excel/PDF – WIP)

---

## 📥 Sample input format (`sample_input.xlsx`)

| Room Name | Category     | Area (m²) | Cost per m² |
|-----------|--------------|-----------|--------------|
| Living A  | Residential  | 70        | 1500         |
| Office B  | Commercial   | 120       | 1800         |

---

## 🚀 Quick Start

```bash
git clone https://github.com/ZverevDmitriyZDV/BimFinance.git
cd BimFinance
pip install -r requirements.txt
streamlit run streamlit_app/main.py
