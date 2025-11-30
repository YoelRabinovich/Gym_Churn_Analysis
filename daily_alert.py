import mysql.connector
import pandas as pd
from datetime import datetime

# 1. Connect to the Database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',          # Your MySQL username
        password='root',      # <--- Ensure this matches your actual password!
        database='gym_project'
    )
    return connection

# 2. Fetch Data from the SQL View
def get_risk_report():
    conn = get_db_connection()
    # querying the view we created earlier
    query = "SELECT * FROM churn_risk_dashboard WHERE Risk_Category = 'Critical Risk'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 3. Generate Alert (Simulation of Email/Slack)
def send_alert(df):
    if df.empty:
        print("✅ No high-risk clients detected today.")
        return

    total_loss_risk = df['Monthly_Fee'].sum()
    num_clients = len(df)
    
    print("="*50)
    print(f"🚨 DAILY CHURN ALERT - {datetime.now().strftime('%d/%m/%Y')}")
    print("="*50)
    print(f"CRITICAL: Identified {num_clients} high-risk clients!")
    print(f"Potential Monthly Loss: {total_loss_risk} NIS")
    print("-" * 30)
    print("Action Items - Call List:")
    
    # Display top 10 at-risk members
    print(df[['Member_ID', 'Plan_Type', 'Avg_Historical', 'Last_Month_Visits']].head(10))
    
    print("..." if num_clients > 10 else "")
    print("="*50)
    
    # Placeholder: In a real production env, will add email/Slack API call here

if __name__ == "__main__":
    print("Connecting to MySQL and fetching data...")
    risk_df = get_risk_report()
    send_alert(risk_df)
