import pandas as pd
from datetime import datetime, timedelta
import json




with open("arcs_gen/init_arcs.json", "r") as file:
    data = json.load(file)
    rows = data["arcs"]


reversed_rows = []
for row in rows:
    reversed_rows.append({
        'From': row['To'],
        'To': row['From'],
        'Day': row['Day'],
        'Time': row['Time'],
        'Distance': row['Distance'],
        'Duration': row['Duration'],
    })

rows.extend(reversed_rows)

cities = []
for row in rows:
    cities.append(row["From"])
    cities.append(row["To"])
cities = list(set(cities))

for city in cities:
    self_arc = {
        'From': city,
        'To': city,
        'Day': '',
        'Time': '08:00:00',
        'Distance': '0 km',
        'Duration': '1 mins',
    }
    rows.append(self_arc)

df = pd.DataFrame(rows)
df["Day"] = "2024-09-02" # the date that data was collected

def insert_rows_below(df):
    result_df = pd.DataFrame()
    for index, row in df.iterrows():
        new_rows = []
        start_time = datetime.strptime(row['Time'], '%H:%M:%S')
        duration_minutes = int(row['Duration'].split()[0])
        end_time = start_time + timedelta(hours=2)

        current_time = start_time + timedelta(minutes=1)
        while current_time + timedelta(minutes=duration_minutes) <= end_time:
            new_row = row.copy()
            new_row['Time'] = current_time.strftime('%H:%M:%S')
            new_rows.append(new_row)
            current_time += timedelta(minutes=1)

        new_df = pd.DataFrame([row] + new_rows)
        result_df = pd.concat([result_df, new_df], ignore_index=True)
    
    return result_df

expanded_df = insert_rows_below(df)
expanded_df.to_csv("arcs.csv", index=False)
