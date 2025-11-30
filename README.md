# 🏋️ Gym Churn Prediction & Retention Analytics

### End-to-End Data Analysis Project | Python -  SQL -  Power BI

![Project Status](https://img.shields.io/badge/Status-Completedhttps://img.shields.io/badge/Tools-Python%20|%20MySQL%20|%20PowerBI
This project delivers a comprehensive analytics solution for tackling gym member churn. It uses customer behavioral data to flag high-risk members—particularly spotting a “Usage Cliff” before cancellations—and automates alerts to support effective retention actions, preventing revenue loss.

## 🎯 The Business Problem
- **Challenge:** Gym churn significantly undermines monthly recurring revenue.
- **Insight:** Most customers stop showing up about a month before formally quitting.
- **Solution:** Automated pipeline detects sudden drops in member activity, labeling “Critical Risk” clients before they cancel.

## 🏗️ Solution Architecture

1. **Data Generation (Python):**
   - Scripted realistic simulation of 1,000 gym members
   - Patterns engineered for seasonality, peak times, and churn
2. **Data Warehousing (MySQL):**
   - Structured relational schema (`members`, `checkins`)
   - SQL View for rollup and trend analytics
3. **Automation & Alerting (Python):**
   - Monitoring bot runs daily, flags zero-visitors with historically high usage
   - Produces prioritized call list with revenue risk calculations
4. **Visualization (Power BI):**
   - Interactive dashboard for stakeholders
   - Core KPIs: Revenue at Risk, Churn vs. Active trends, Drill-down member lists

## 📊 Dashboard Preview
*(Insert screenshot of Power BI dashboard visualizing churn metrics and risk KPIs.)*

## 🛠️ Technologies Used

- **Python:** Pandas, Numpy, Faker, MySQL-Connector (ETL/Simulation)
- **SQL (MySQL):** Advanced queries, window functions, data cleaning
- **Power BI:** Data modeling, DAX KPIs, interactive reporting

## 🚀 How to Run This Project

### 1. Database Setup
Use `gym_churn_analysis.sql` in MySQL to deploy schema and views.

### 2. Generate Data
Populate DB with:
```bash
python data_generator.py
```

### 3. Run the Analytics Bot
Detect at-risk customers:
```bash
python daily_alert.py
```

### 4. View the Dashboard
Open `Gym_Retention_Dashboard.pbix` in Power BI Desktop and refresh to see data.

**Author:** Joel, Open University Graduate (B.Sc. Computer Science)

***
