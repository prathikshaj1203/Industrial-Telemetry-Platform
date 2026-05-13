import pandas as pd
import psycopg2
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

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
# LOAD TELEMETRY DATA
# ==========================================

query = """
SELECT *
FROM telemetry_data
ORDER BY timestamp
"""

df = pd.read_sql(query, connection)

print("\nDATA LOADED SUCCESSFULLY\n")

# ==========================================
# CREATE FUTURE FAILURE LABELS
# ==========================================

df['future_failure'] = 0

window_size = 5

for i in range(len(df) - window_size):

    future_window = df.iloc[i:i + window_size]

    if (
        future_window['temperature'].max() > 95 or
        future_window['vibration'].max() > 0.9 or
        future_window['power_usage'].max() > 750
    ):

        df.loc[i, 'future_failure'] = 1

print("\nFUTURE FAILURE LABELS CREATED\n")

# ==========================================
# FEATURES
# ==========================================

features = [
    'temperature',
    'vibration',
    'pressure',
    'rpm',
    'power_usage'
]

X = df[features]

# TARGET VARIABLE
y = df['future_failure']

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# MODEL TRAINING
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("\nMODEL TRAINED SUCCESSFULLY\n")

# ==========================================
# PREDICTIONS
# ==========================================

predictions = model.predict(X_test)

print("\nCLASSIFICATION REPORT\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# ==========================================
# FAILURE PROBABILITY
# ==========================================

df['failure_probability'] = model.predict_proba(X)[:, 1]

# ==========================================
# HIGH RISK MACHINES
# ==========================================

high_risk = df[
    df['failure_probability'] > 0.7
]

print("\nHIGH RISK MACHINES DETECTED\n")

print(
    high_risk[
        [
            'machine_id',
            'temperature',
            'vibration',
            'power_usage',
            'failure_probability'
        ]
    ].head(20)
)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    'predictive_maintenance_model.pkl'
)

print("\nMODEL SAVED SUCCESSFULLY\n")