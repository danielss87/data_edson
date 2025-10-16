import pandas as pd
from datetime import datetime

# Lendo o CSV
df = pd.read_csv("data/processed/videos_processed.csv")

# Convertendo duration_readable de HH:MM:SS para minutos
def duration_to_minutes(duration_str):
    try:
        h, m, s = map(int, duration_str.split(':'))
        return h * 60 + m + s / 60
    except:
        return 0

df['duration_minutes'] = df['duration_readable'].apply(duration_to_minutes)

# Convertendo Published At para datetime
df['Published At'] = pd.to_datetime(df['Published At'])

# Calculando meses desde o lançamento até hoje
today = pd.to_datetime('today')
df['months_since_release'] = ((today.year - df['Published At'].dt.year) * 12 + 
                              (today.month - df['Published At'].dt.month))
# Evitar divisão por zero
df['months_since_release'] = df['months_since_release'].replace(0, 1)

# Criando a nova feature 'views_por_mes'
df['views_por_mes'] = df['Views'] / df['months_since_release']

# Arredondando para inteiro
df['views_por_mes'] = df['views_por_mes'].round(0).astype(int)

# Salvando de volta para CSV
df.to_csv("data/processed/videos_processed_with_views_per_month.csv", index=False)

print(df[['Views', 'Published At', 'months_since_release', 'views_por_mes']].head())
