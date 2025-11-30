import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- General Configuration ---
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

# --- Step 1: Generate Members Table ---
members = []

for i in range(1, NUM_MEMBERS + 1):
    join_date = START_DATE + timedelta(days=random.randint(0, 600))
    plan = random.choice(plans)
    
    # Churn Logic: 30% of members will eventually churn
    is_churned = random.random() < 0.3
    churn_date = None
    status = 'Active'
    
    if is_churned:
        # Retention typically lasts between 3 to 8 months
        retention_days = random.randint(90, 240)
        churn_date = join_date + timedelta(days=retention_days)
        
        # If the calculated churn date is in the future (beyond simulation end), reset to Active
        if churn_date > END_DATE:
            churn_date = None
            is_churned = False
        else:
            status = 'Churned'
            
    members.append({
        'Member_ID': i,
        'Age': random.randint(18, 65),
        'Gender': random.choice(['M', 'F']),
        'City': random.choices(cities, weights=[40, 20, 15, 15, 10])[0], # Weighted to favor Tel Aviv
        'Join_Date': join_date.strftime('%Y-%m-%d'), 
        'Plan_Type': plan['name'],
        'Monthly_Fee': plan['price'],
        'Status': status,
        
        # FIX: Use a placeholder future date (2099) for NULL values 
        # to prevent CSV import errors in MySQL Wizards.
        'Churn_Date': churn_date.strftime('%Y-%m-%d') if churn_date else '2099-12-31' 
    })

df_members = pd.DataFrame(members)

# --- Step 2: Generate Check-ins Table ---
checkins = []

for index, member in df_members.iterrows():
    # Convert string dates back to datetime objects for calculations
    member_join_date = datetime.strptime(member['Join_Date'], '%Y-%m-%d')
    
    # Handle the placeholder date for active members
    if member['Churn_Date'] == '2099-12-31':
         active_end_date = END_DATE
    else:
         active_end_date = datetime.strptime(member['Churn_Date'], '%Y-%m-%d')

    # The "Cliff" Logic: Churned users stop working out 2-6 weeks BEFORE cancelling
    if member['Status'] == 'Churned':
        stop_workout_buffer = timedelta(days=random.randint(14, 45))
        workout_end_date = active_end_date - stop_workout_buffer
    else:
        workout_end_date = active_end_date

    current_date = member_join_date
    
    # Generate random check-ins based on realistic behavior
    while current_date < workout_end_date:
        # Frequency: Exponential distribution (avg 3.5 days gap between workouts)
        days_skip = int(np.random.exponential(scale=3.5)) 
        current_date += timedelta(days=max(1, days_skip))
        
        if current_date < workout_end_date:
            # Assign hours based on plan type and realistic peak times
            if member['Plan_Type'] == 'Morning':
                hour = random.randint(6, 15)
            else:
                # Weighted random choice for peak hours (Morning & Evening peaks)
                hour = random.choices(
                    [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
                    weights=[5,10,10,5,3,2,2,2,3,4,4,10,15,15,8,2,1]
                )[0]
                
            checkins.append({
                'Checkin_ID': len(checkins) + 1,
                'Member_ID': member['Member_ID'],
                'Checkin_Date': current_date.strftime('%Y-%m-%d'), # Formatted for MySQL
                'Time': f"{hour:02d}:{random.randint(0,59):02d}",
                'Weekday': current_date.strftime('%A')
            })

df_checkins = pd.DataFrame(checkins)

# --- Save Files ---
df_members.to_csv('gym_members.csv', index=False)
df_checkins.to_csv('gym_checkins.csv', index=False)

print("Success! Files 'gym_members.csv' and 'gym_checkins.csv' generated in MySQL-compatible format.")
