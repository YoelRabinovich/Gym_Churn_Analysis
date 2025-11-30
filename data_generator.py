import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# הגדרות כלליות
NUM_MEMBERS = 1000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

cities = ['Tel Aviv', 'Ramat Gan', 'Givatayim', 'Petah Tikva', 'Herzliya']
plans = [
    {'name': 'Basic', 'price': 199, 'access': 'All Day'},
    {'name': 'Premium', 'price': 299, 'access': 'All Day + Classes'},
    {'name': 'Morning', 'price': 149, 'access': 'Until 16:00'},
    {'name': 'Student', 'price': 180, 'access': 'All Day'}
]

# --- שלב 1: יצירת טבלת מנויים (Members) ---
members = []

for i in range(1, NUM_MEMBERS + 1):
    join_date = START_DATE + timedelta(days=random.randint(0, 600))
    plan = random.choice(plans)
    
    is_churned = random.random() < 0.3
    churn_date = None
    status = 'Active'
    
    if is_churned:
        retention_days = random.randint(90, 240)
        churn_date = join_date + timedelta(days=retention_days)
        if churn_date > END_DATE:
            churn_date = None
            is_churned = False
        else:
            status = 'Churned'
            
# --- בתוך לולאת ה-Members ---

    # ... (כל הקוד הקודם נשאר אותו דבר)

    members.append({
        'Member_ID': i,
        'Age': random.randint(18, 65),
        'Gender': random.choice(['M', 'F']),
        'City': random.choices(cities, weights=[40, 20, 15, 15, 10])[0],
        'Join_Date': join_date.strftime('%Y-%m-%d'), 
        'Plan_Type': plan['name'],
        'Monthly_Fee': plan['price'],
        'Status': status,
        
        # === התיקון נמצא בשורה הזו ===
        # אם אין תאריך נטישה, נשים תאריך עתידי (2099) כדי שהייבוא יעבוד
        'Churn_Date': churn_date.strftime('%Y-%m-%d') if churn_date else '2099-12-31' 
    })
df_members = pd.DataFrame(members)

# --- שלב 2: יצירת טבלת כניסות (Check-ins) ---
checkins = []

for index, member in df_members.iterrows():
    # המרה חזרה ל-datetime כדי לעשות חישובים (כי למעלה הפכנו לסטרינג)
    member_join_date = datetime.strptime(member['Join_Date'], '%Y-%m-%d')
    member_churn_date = datetime.strptime(member['Churn_Date'], '%Y-%m-%d') if member['Churn_Date'] else None
    
    active_end_date = member_churn_date if member['Status'] == 'Churned' else END_DATE
    
    if member['Status'] == 'Churned':
        stop_workout_buffer = timedelta(days=random.randint(14, 45))
        workout_end_date = active_end_date - stop_workout_buffer
    else:
        workout_end_date = active_end_date

    current_date = member_join_date
    while current_date < workout_end_date:
        days_skip = int(np.random.exponential(scale=3.5)) 
        current_date += timedelta(days=max(1, days_skip))
        
        if current_date < workout_end_date:
            if member['Plan_Type'] == 'Morning':
                hour = random.randint(6, 15)
            else:
                hour = random.choices(
                    [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
                    weights=[5,10,10,5,3,2,2,2,3,4,4,10,15,15,8,2,1]
                )[0]
                
            checkins.append({
                'Checkin_ID': len(checkins) + 1,
                'Member_ID': member['Member_ID'],
                
                # --- תיקון כאן: המרת תאריך לפורמט YYYY-MM-DD ---
                'Checkin_Date': current_date.strftime('%Y-%m-%d'),
                
                'Time': f"{hour:02d}:{random.randint(0,59):02d}",
                'Weekday': current_date.strftime('%A')
            })

df_checkins = pd.DataFrame(checkins)

# --- שמירת הקבצים ---
df_members.to_csv('gym_members.csv', index=False)
df_checkins.to_csv('gym_checkins.csv', index=False)

print("הקבצים נוצרו בפורמט YYYY-MM-DD שמתאים ל-MySQL!")