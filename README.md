# 🏋️ Gym Churn Prediction & Retention Analytics

### End-to-End Data Analysis Project | Python • SQL • Power BI

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Tools](https://img.shields.io/badge/Tools-Python%20|%20MySQL%20|%20PowerBI-blue)

## 📖 Overview
This project is a full-stack data analytics solution designed to tackle customer churn in the fitness industry. 
The system identifies high-risk members based on behavioral patterns (specifically the "Usage Cliff" phenomenon) and generates automated alerts for retention teams to intervene before a subscription is cancelled.

## 🎯 The Business Problem
* **The Challenge:** High churn rates in gyms significantly impact monthly recurring revenue (MRR).
* **The Insight:** Most members stop attending the gym approx. 30 days before officially cancelling their membership.
* **The Solution:** An automated pipeline that detects this drop in activity in real-time and flags "Critical Risk" customers.

## 🏗️ Solution Architecture
The project follows a classic ETL and Analytics pipeline:

1.  **Data Generation (Python):** * Created a script (`data_generator.py`) to simulate a realistic gym database with 1,000 members.
    * Engineered specific statistical distributions to mimic seasonality, peak hours, and churn behavior.
2.  **Data Warehousing (MySQL):** * Designed a relational schema (`members`, `checkins`).
    * Built a complex SQL View (`churn_risk_dashboard`) to calculate rolling averages and activity trends.
3.  **Automation & Alerting (Python):**
    * Developed a monitoring bot (`daily_alert.py`) that queries the DB daily.
    * Identifies users with `0 visits` in the last 30 days vs. high historical average.
    * Outputs a "Call List" with potential revenue loss calculations.
4.  **Visualization (Power BI):**
    * Interactive dashboard for stakeholders.
    * Key features: Revenue at Risk KPI, Churn vs. Active trend lines, and drill-down lists.

## 📊 Dashboard Preview
*(Add a screenshot of your Power BI dashboard here)*

## 🛠️ Technologies Used
* **Python:** Pandas, Numpy, Faker, MySQL-Connector (Data generation & ETL).
* **SQL (MySQL):** Complex queries, Window Functions, Views, Data Cleaning.
* **Power BI:** Data Modeling, DAX Measures, Interactive Visualization.

## 🚀 How to Run This Project

### 1. Database Setup
Run the SQL script `gym_churn_analysis.sql` in your MySQL environment to create the schema and the analytical views.

### 2. Generate Data
Run the Python data generator to populate the database with synthetic data:
```bash
python data_generator.py
### 3. Run the Analytics Bot
Execute the alert script to identify at-risk customers for the current date: python daily_alert.py
### 4. View the Dashboard
Open Gym_Retention_Dashboard.pbix in Power BI Desktop and hit "Refresh" to load the latest data from your local MySQL database.

Author: Joel Open University Graduate (B.Sc. Computer Science)