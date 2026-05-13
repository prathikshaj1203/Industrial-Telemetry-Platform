import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from sklearn.ensemble import IsolationForest
import joblib
from dotenv import load_dotenv
import os

load_dotenv()

def calculate_health(row):

    score = 100

    # Temperature
    if row['temperature'] > 100:
        score -= 50
    elif row['temperature'] > 85:
        score -= 30
    elif row['temperature'] > 70:
        score -= 10

    # Vibration
    if row['vibration'] > 1.0:
        score -= 30
    elif row['vibration'] > 0.7:
        score -= 20
    elif row['vibration'] > 0.4:
        score -= 10

    # Pressure
    if row['pressure'] < 20:
        score -= 15

    # RPM
    if row['rpm'] < 700:
        score -= 10

    # Power usage
    if row['power_usage'] > 700:
        score -= 25
    elif row['power_usage'] > 550:
        score -= 10

    return max(score, 0)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Industrial Telemetry Dashboard",
    layout="wide"
)

# Auto Refresh Every 5 Seconds
st_autorefresh(interval=5000, key="telemetryrefresh")

# ==========================================
# TITLE
# ==========================================

st.title("🏭 Industrial Telemetry Monitoring Dashboard")
st.caption(
    f"🕒 Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
# ==========================================
# LOAD TRAINED AI MODEL
# ==========================================

predictive_model = joblib.load(
    'ai-models/predictive_maintenance_model.pkl'
)
# ==========================================
# FETCH DATA
# ==========================================

query = """
SELECT *
FROM telemetry_data
ORDER BY timestamp DESC
LIMIT 100
"""

df = pd.read_sql(query, connection)

# Convert Timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['health_score'] = df.apply(calculate_health, axis=1)

# ==========================================
# LIVE FAILURE PREDICTION
# ==========================================

prediction_features = df[
    [
        'temperature',
        'vibration',
        'pressure',
        'rpm',
        'power_usage'
    ]
]

df['failure_probability'] = (
    predictive_model.predict_proba(prediction_features)[:, 1]
)

df['failure_percentage'] = (
    df['failure_probability'] * 100
).round(2)

def risk_level(prob):

    if prob >= 90:
        return "🔴 CRITICAL"

    elif prob >= 70:
        return "🟡 HIGH"

    elif prob >= 40:
        return "🟢 MODERATE"

    return "✅ LOW"

df['risk_level'] = df[
    'failure_percentage'
].apply(risk_level)

# ==========================================
# AI ANOMALY DETECTION
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

anomaly_model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df['anomaly'] = anomaly_model.fit_predict(features)

df['anomaly'] = df['anomaly'].map({
    1: 'NORMAL',
    -1: 'ANOMALY'
})

# ==========================================
# KPI METRICS
# ==========================================

total_machines = df['machine_id'].nunique()
critical_count = len(df[df['state'] == 'CRITICAL'])
warning_count = len(df[df['state'] == 'WARNING'])
normal_count = len(df[df['state'] == 'NORMAL'])

avg_temp = round(df['temperature'].mean(), 2)
avg_vibration = round(df['vibration'].mean(), 2)
high_risk_count = len(
    df[df['failure_probability'] > 0.7]
)

ai_anomalies = len(df[df['anomaly'] == 'ANOMALY'])

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("🏭 Total Machines", total_machines)
col2.metric("🚨 Critical Alerts", critical_count)
col3.metric("🌡 Avg Temperature", avg_temp)
col4.metric("📈 Avg Vibration", avg_vibration)
col5.metric("🤖 AI Anomalies", ai_anomalies)
col6.metric(
    "🤖 Predicted Failures",
    high_risk_count
)
highest_risk = round(
    df['failure_percentage'].max(),
    2
)

col7.metric(
    "🔥 Highest Failure Risk",
    f"{highest_risk}%"
)
st.markdown("---")
# ==========================================
# LIVE SYSTEM RISK OVERVIEW
# ==========================================

st.subheader("🔥 Live System Risk Overview")

risk_chart = px.scatter(
    df,
    x='temperature',
    y='vibration',
    size='failure_percentage',
    color='risk_level',
    hover_data=['machine_id'],
    title='AI Risk Intelligence Map'
)

st.plotly_chart(
    risk_chart,
    width="stretch"
)
# ==========================================
# PREDICTIVE MAINTENANCE
# ==========================================

st.subheader("🤖 Predictive Maintenance Intelligence")

high_risk_df = df[
    df['failure_probability'] > 0.7
]

prediction_table = high_risk_df[
    [
        'machine_id',
        'temperature',
        'vibration',
        'power_usage',
        'failure_percentage',
        'risk_level'
    ]
]

prediction_table = prediction_table.sort_values(
    by='failure_percentage',
    ascending=False
)

prediction_table = prediction_table.drop_duplicates(
    subset='machine_id'
)

st.dataframe(
    prediction_table.head(10),
    use_container_width=True
)

# ==========================================
# AI DETECTED ANOMALIES
# ==========================================

st.subheader("🤖 AI Detected Machine Anomalies")

anomaly_df = df[df['anomaly'] == 'ANOMALY']

if len(anomaly_df) > 0:

    st.error("AI detected abnormal machine behavior!")

    st.dataframe(
        anomaly_df[
            [
                'machine_id',
                'temperature',
                'vibration',
                'pressure',
                'rpm',
                'power_usage',
                'anomaly'
            ]
        ],
        use_container_width=True
    )

else:
    st.success("No AI anomalies detected.")

# ==========================================
# MACHINE STATUS OVERVIEW
# ==========================================

st.subheader("🛠 Machine Status Overview")

c1, c2, c3 = st.columns(3)

c1.success(f"🟢 NORMAL: {normal_count}")
c2.warning(f"🟡 WARNING: {warning_count}")
c3.error(f"🔴 CRITICAL: {critical_count}")

st.markdown("---")

# ==========================================
# LIVE TELEMETRY TABLE
# ==========================================

with st.expander("📡 View Live Machine Telemetry"):

    st.dataframe(
        df.head(150),
        width="stretch"
    )
st.subheader("💚 Machine Health Scores")

health_df = (
    df.sort_values(by='timestamp', ascending=False)
      .drop_duplicates(subset='machine_id')
)

health_df = health_df[
    ['machine_id', 'machine_type', 'health_score', 'state']
].sort_values(by='health_score')

display_df = df[
    [
        'machine_id',
        'machine_type',
        'state',
        'temperature',
        'vibration',
        'pressure',
        'rpm',
        'power_usage',
        'health_score',
        'timestamp',
        'failure_percentage',
        'risk_level',
        'anomaly'
    ]
]

display_df = display_df.sort_values(
    by='failure_percentage',
    ascending=False
)

st.dataframe(
    display_df.head(50),
    use_container_width=True
)

health_chart = px.bar(
    health_df,
    x='machine_id',
    y='health_score',
    color='health_score',
    title='Machine Health Score Analysis',
    text='health_score'
)

health_chart.update_layout(
    xaxis_title="Machine ID",
    yaxis_title="Health Score",
)

st.plotly_chart(
    health_chart,
    use_container_width=True
)

# ==========================================
# MACHINE HEALTH DISTRIBUTION
# ==========================================

state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['State', 'Count']

fig1 = px.pie(
    state_counts,
    names='State',
    values='Count',
    title='Machine Health Distribution'
)

st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# TEMPERATURE MONITORING
# ==========================================

st.subheader("🌡 Temperature Monitoring")

fig2 = px.line(
    df,
    x='timestamp',
    y='temperature',
    color='machine_id',
    title='Temperature Trends',
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# VIBRATION MONITORING
# ==========================================

st.subheader("📈 Vibration Monitoring")

fig3 = px.line(
    df,
    x='timestamp',
    y='vibration',
    color='machine_id',
    title='Vibration Trends',
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# POWER USAGE MONITORING
# ==========================================

st.subheader("⚡ Power Consumption Monitoring")

fig4 = px.area(
    df,
    x='timestamp',
    y='power_usage',
    color='machine_id',
    title='Power Usage Trends'
)

st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# MACHINE FILTER
# ==========================================

st.sidebar.header("🔍 Machine Filter")

selected_machine = st.sidebar.selectbox(
    "Select Machine ID",
    options=["All"] + list(df['machine_id'].unique())
)

if selected_machine != "All":
    filtered_df = df[df['machine_id'] == selected_machine]

    st.subheader(f"🖥 Detailed Analytics for {selected_machine}")

    st.dataframe(filtered_df, use_container_width=True)

# ==========================================
# CRITICAL MACHINE ALERTS
# ==========================================

critical_df = df[df['state'] == 'CRITICAL']

st.subheader("🚨 Critical Machine Alerts")

if len(critical_df) > 0:
    st.error("Critical machines detected!")

    st.dataframe(
        critical_df,
        use_container_width=True
    )

else:
    st.success("No critical machines currently.")

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption("⚙ Real-Time Industrial Telemetry Monitoring System")

connection.close()