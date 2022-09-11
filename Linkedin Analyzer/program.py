import pandas as pd
from datetime import datetime
import json

df = pd.read_csv('Connections.csv', skiprows=2)

def fix_dates(date):
    date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")
    return date

df['Connected On'] = df['Connected On'].apply(fix_dates)

df_companies = df.groupby('Company', as_index=False).agg({'First Name':'count'})
df_companies = df_companies.rename(columns={'First Name' : 'count'})
df_companies = df_companies.sort_values('count', ascending=False)

df_position = df.groupby('Position', as_index=False).agg({'First Name':'count'})
df_position = df_position.rename(columns={'First Name' : 'count'})
df_position = df_position.sort_values('count', ascending=False)
df_position.head(10)

m = datetime.today().month
if m<10:
    month = '0'+str(m)
else:
    month = str(m)
year = str(datetime.today().year)
new_connections = df[df['Connected On']>=f'{year}-{month}-01']

final_json = {}

final_json['total_connections'] = len(df)
final_json['new connections this month'] = len(new_connections)
final_json['top 10 companies'] = df_companies.head(10).to_dict('records')
final_json['top 10 positions'] = df_position.head(10).to_dict('records')
final_json['last 10 connections'] = df.sort_values('Connected On', ascending=False).head(10)[['First Name', 'Last Name', 'Connected On']].to_dict('records')
final_json['first connected with'] = df.sort_values('Connected On').head(1)[['First Name', 'Last Name', 'Connected On']].to_dict('records')
final_json['last connected with'] = df.sort_values('Connected On', ascending=False).head(1)[['First Name', 'Last Name', 'Connected On']].to_dict('records')
final_json['cold email'] = df[~df['Email Address'].isna()].to_dict('records')

json_object = json.dumps(final_json, indent = 4)

print(json_object)
