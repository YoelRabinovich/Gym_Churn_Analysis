import mysql.connector
import pandas as pd

# 1. חיבור לבסיס הנתונים
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',         # המשתמש שלך
        password='root', # <--- שים כאן את הסיסמה שלך!
        database='gym_project'
    )
    return connection

# 2. שליפת הנתונים מה-VIEW שיצרנו
def get_risk_report():
    conn = get_db_connection()
    query = "SELECT * FROM churn_risk_dashboard WHERE Risk_Category = 'Critical Risk'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 3. יצירת ההתראה (סימולציה של שליחת מייל)
def send_alert(df):
    if df.empty:
        print("✅ אין היום לקוחות בסיכון גבוה.")
        return

    total_loss_risk = df['Monthly_Fee'].sum()
    num_clients = len(df)
    
    print("="*50)
    print(f"🚨 DAILY CHURN ALERT - {pd.Timestamp.now().strftime('%d/%m/%Y')}")
    print("="*50)
    print(f"CRITICAL: Identified {num_clients} high-risk clients!")
    print(f"Potential Monthly Loss:{total_loss_risk} ₪")
    print("-" * 30)
    print("Action Items - Call List:")
    print(df[['Member_ID', 'Plan_Type', 'Avg_Historical', 'Last_Month_Visits']].head(10)) # מציג רק 10 ראשונים
    print("..." if num_clients > 10 else "")
    print("="*50)
    
    # כאן בעתיד אפשר להוסיף פונקציה ששולחת את זה למייל או ל-Slack

if __name__ == "__main__":
    print("מתחבר ל-MySQL ושולף נתונים...")
    risk_df = get_risk_report()
    send_alert(risk_df)