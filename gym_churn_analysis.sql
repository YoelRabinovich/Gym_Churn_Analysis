/*
Project: Gym Churn Prediction & Analytics
Author: Joel (Your Last Name)
Description: This script sets up the database schema and creates the analytical view 
used for the churn prediction dashboard and Python alert system.
*/

-- Step 1: Create the Database Schema
CREATE DATABASE IF NOT EXISTS gym_project;
USE gym_project;

-- Create Members Table
CREATE TABLE IF NOT EXISTS members (
    Member_ID INT PRIMARY KEY,
    Age INT,
    Gender CHAR(1),
    City VARCHAR(50),
    Join_Date DATE,
    Plan_Type VARCHAR(20),
    Monthly_Fee INT,
    Status VARCHAR(20),
    Churn_Date DATE NULL
);

-- Create Check-ins Table
CREATE TABLE IF NOT EXISTS checkins (
    Checkin_ID INT PRIMARY KEY,
    Member_ID INT,
    Checkin_Date DATE,
    Time VARCHAR(10),
    Weekday VARCHAR(10),
    FOREIGN KEY (Member_ID) REFERENCES members(Member_ID)
);

-- (Data is loaded via Python script or CSV import at this stage)

-- Step 2: Data Cleaning Logic (Handling Import Issues)
SET SQL_SAFE_UPDATES = 0;
UPDATE members SET Churn_Date = NULL WHERE Churn_Date = '2099-12-31';
SET SQL_SAFE_UPDATES = 1;

-- Step 3: Create the Analytical View (The Business Logic)
-- This view calculates rolling attendance and flags high-risk users based on usage drops.
CREATE OR REPLACE VIEW churn_risk_dashboard AS
WITH Constants AS (
    -- Simulation Date set to June 2024 to catch churners before they leave
    SELECT '2024-06-01' AS report_date
),
User_Stats AS (
    SELECT 
        m.Member_ID,
        m.Plan_Type,
        m.Monthly_Fee,
        -- Calculate visits in the last 30 days relative to report date
        COUNT(CASE WHEN c.Checkin_Date > DATE_SUB(const.report_date, INTERVAL 30 DAY) THEN 1 END) AS Last_Month_Visits,
        
        -- Calculate average monthly visits prior to the last month
        COUNT(CASE WHEN c.Checkin_Date <= DATE_SUB(const.report_date, INTERVAL 30 DAY) THEN 1 END) / 
        GREATEST(TIMESTAMPDIFF(MONTH, m.Join_Date, DATE_SUB(const.report_date, INTERVAL 30 DAY)), 1) AS Avg_Monthly_Visits
    FROM members m
    CROSS JOIN Constants const
    LEFT JOIN checkins c ON m.Member_ID = c.Member_ID
    WHERE m.Status = 'Active' OR m.Churn_Date > const.report_date 
    GROUP BY m.Member_ID, m.Plan_Type, m.Monthly_Fee, m.Join_Date, const.report_date
)
SELECT 
    Member_ID,
    Plan_Type,
    Monthly_Fee,
    Last_Month_Visits,
    ROUND(Avg_Monthly_Visits, 1) AS Avg_Historical,
    -- Calculate percentage change in behavior
    ROUND(((Last_Month_Visits - Avg_Monthly_Visits) / NULLIF(Avg_Monthly_Visits, 0)) * 100, 0) AS Trend_Pct,
    -- Define Risk Categories
    CASE 
        WHEN Last_Month_Visits = 0 AND Avg_Monthly_Visits >= 2 THEN 'Critical Risk'
        WHEN Last_Month_Visits < (Avg_Monthly_Visits * 0.5) THEN 'High Risk'
        ELSE 'Safe' 
    END AS Risk_Category
FROM User_Stats;