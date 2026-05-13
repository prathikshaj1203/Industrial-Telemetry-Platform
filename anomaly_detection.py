import pandas as pd
import psycopg2

from sklearn.ensemble import IsolationForest

# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = psycopg2.connect(
    host="localhost",
    database="telemetry_db",
    user="postgres",
    password="root1234",
    port="5432"
)

# ==========================================
# FETCH DATA
# ==========================================

query = """
SELECT *
FROM telemetry_data
ORDER BY timestamp DESC
LIMIT 1000
"""

df = pd.read_sql(query, connection)

# ==========================================
# SELECT FEATURES
# ==========================================

features = df[
    [
        'temperature',
        'vibration',
        'pressure',
        'rpm',
        'power_usage'
    ]
]

# ==========================================
# TRAIN MODEL
# ==========================================

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df['anomaly'] = model.fit_predict(features)

# ==========================================
# CONVERT PREDICTIONS
# ==========================================

df['anomaly'] = df['anomaly'].map({
    1: 'NORMAL',
    -1: 'ANOMALY'
})

# ==========================================
# SHOW ANOMALIES
# ==========================================

anomalies = df[df['anomaly'] == 'ANOMALY']

print("\n🚨 ANOMALIES DETECTED:\n")

print(
    anomalies[
        [
            'machine_id',
            'temperature',
            'vibration',
            'pressure',
            'rpm',
            'power_usage',
            'anomaly'
        ]
    ]
)

connection.close()