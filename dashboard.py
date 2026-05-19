# import streamlit as st
# import pandas as pd
# import psycopg2
# import plotly.express as px
# from streamlit_autorefresh import st_autorefresh
# from sklearn.ensemble import IsolationForest
# import joblib
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def calculate_health(row):

#     score = 100

#     # Temperature
#     if row['temperature'] > 100:
#         score -= 50
#     elif row['temperature'] > 85:
#         score -= 30
#     elif row['temperature'] > 70:
#         score -= 10

#     # Vibration
#     if row['vibration'] > 1.0:
#         score -= 30
#     elif row['vibration'] > 0.7:
#         score -= 20
#     elif row['vibration'] > 0.4:
#         score -= 10

#     # Pressure
#     if row['pressure'] < 20:
#         score -= 15

#     # RPM
#     if row['rpm'] < 700:
#         score -= 10

#     # Power usage
#     if row['power_usage'] > 700:
#         score -= 25
#     elif row['power_usage'] > 550:
#         score -= 10

#     return max(score, 0)

# # ==========================================
# # PAGE CONFIG
# # ==========================================

# st.set_page_config(
#     page_title="Industrial Telemetry Dashboard",
#     layout="wide"
# )

# # Auto Refresh Every 5 Seconds
# st_autorefresh(interval=5000, key="telemetryrefresh")

# # ==========================================
# # TITLE
# # ==========================================

# st.title("🏭 Industrial Telemetry Monitoring Dashboard")
# st.caption(
#     f"🕒 Last Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
# )
# # ==========================================
# # DATABASE CONNECTION
# # ==========================================

# connection = psycopg2.connect(
#     host=os.getenv("DB_HOST"),
#     database=os.getenv("DB_NAME"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     port=os.getenv("DB_PORT")
# )
# # ==========================================
# # LOAD TRAINED AI MODEL
# # ==========================================

# predictive_model = joblib.load(
#     'ai-models/predictive_maintenance_model.pkl'
# )
# # ==========================================
# # FETCH DATA
# # ==========================================

# query = """
# SELECT *
# FROM telemetry_data
# ORDER BY timestamp DESC
# LIMIT 100
# """

# filtered_df = pd.read_sql(query, connection)

# # ==========================================
# # MACHINE CATEGORY FILTER
# # ==========================================

# st.sidebar.header("🏭 Machine Category Filter")

# categories = filtered_df["machine_category"].unique()

# selected_category = st.sidebar.selectbox(

#     "Select Machine Category",

#     ["All"] + list(categories)

# )

# if selected_category != "All":

#     filtered_df = df[
#         df["machine_category"] == selected_category
#     ]

# else:

#     filtered_df = df

# # =====================================
# # LIVE MACHINE STATUS SUMMARY
# # =====================================

# total_machines = df["machine_id"].nunique()

# normal_count = len(
#     df[df["state"] == "NORMAL"]
# )

# warning_count = len(
#     df[df["state"] == "WARNING"]
# )

# critical_count = len(
#     df[df["state"] == "CRITICAL"]
# )

# # =====================================
# # METRICS ROW
# # =====================================

# col1, col2, col3, col4 = st.columns(4)

# col1.metric(
#     "Total Machines",
#     total_machines
# )

# col2.metric(
#     "Normal",
#     normal_count
# )

# col3.metric(
#     "Warnings",
#     warning_count
# )

# col4.metric(
#     "Critical",
#     critical_count
# )

# # Convert Timestamp
# df['timestamp'] = pd.to_datetime(df['timestamp'])
# df['health_score'] = df.apply(calculate_health, axis=1)

# # ==========================================
# # LIVE FAILURE PREDICTION
# # ==========================================

# prediction_features = df[
#     [
#         'temperature',
#         'vibration',
#         'pressure',
#         'rpm',
#         'power_usage'
#     ]
# ]

# df['failure_probability'] = (
#     predictive_model.predict_proba(prediction_features)[:, 1]
# )

# df['failure_percentage'] = (
#     df['failure_probability'] * 100
# ).round(2)

# def risk_level(prob):

#     if prob >= 90:
#         return "🔴 CRITICAL"

#     elif prob >= 70:
#         return "🟡 HIGH"

#     elif prob >= 40:
#         return "🟢 MODERATE"

#     return "✅ LOW"

# df['risk_level'] = df[
#     'failure_percentage'
# ].apply(risk_level)

# # ==========================================
# # AI ANOMALY DETECTION
# # ==========================================

# features = df[
#     [
#         'temperature',
#         'vibration',
#         'pressure',
#         'rpm',
#         'power_usage'
#     ]
# ]

# anomaly_model = IsolationForest(
#     contamination=0.05,
#     random_state=42
# )

# df['anomaly'] = anomaly_model.fit_predict(features)

# df['anomaly'] = df['anomaly'].map({
#     1: 'NORMAL',
#     -1: 'ANOMALY'
# })

# # ==========================================
# # KPI METRICS
# # ==========================================

# total_machines = df['machine_id'].nunique()
# critical_count = len(df[df['state'] == 'CRITICAL'])
# warning_count = len(df[df['state'] == 'WARNING'])
# normal_count = len(df[df['state'] == 'NORMAL'])

# avg_temp = round(df['temperature'].mean(), 2)
# avg_vibration = round(df['vibration'].mean(), 2)
# high_risk_count = len(
#     df[df['failure_probability'] > 0.7]
# )

# ai_anomalies = len(df[df['anomaly'] == 'ANOMALY'])

# col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

# col1.metric("🏭 Total Machines", total_machines)
# col2.metric("🚨 Critical Alerts", critical_count)
# col3.metric("🌡 Avg Temperature", avg_temp)
# col4.metric("📈 Avg Vibration", avg_vibration)
# col5.metric("🤖 AI Anomalies", ai_anomalies)
# col6.metric(
#     "🤖 Predicted Failures",
#     high_risk_count
# )
# highest_risk = round(
#     df['failure_percentage'].max(),
#     2
# )

# col7.metric(
#     "🔥 Highest Failure Risk",
#     f"{highest_risk}%"
# )
# st.markdown("---")
# # ==========================================
# # LIVE SYSTEM RISK OVERVIEW
# # ==========================================

# st.subheader("🔥 Live System Risk Overview")

# risk_chart = px.scatter(
#     df,
#     x='temperature',
#     y='vibration',
#     size='failure_percentage',
#     color='risk_level',
#     hover_data=['machine_id'],
#     title='AI Risk Intelligence Map'
# )

# st.plotly_chart(
#     risk_chart,
#     width="stretch"
# )
# # ==========================================
# # PREDICTIVE MAINTENANCE
# # ==========================================

# st.subheader("🤖 Predictive Maintenance Intelligence")

# high_risk_df = df[
#     df['failure_probability'] > 0.7
# ]

# prediction_table = high_risk_df[
#     [
#         'machine_id',
#         'temperature',
#         'vibration',
#         'power_usage',
#         'failure_percentage',
#         'risk_level'
#     ]
# ]

# prediction_table = prediction_table.sort_values(
#     by='failure_percentage',
#     ascending=False
# )

# prediction_table = prediction_table.drop_duplicates(
#     subset='machine_id'
# )

# st.dataframe(
#     prediction_table.head(10),
#     use_container_width=True
# )

# # ==========================================
# # AI DETECTED ANOMALIES
# # ==========================================

# st.subheader("🤖 AI Detected Machine Anomalies")

# anomaly_df = df[df['anomaly'] == 'ANOMALY']

# if len(anomaly_df) > 0:

#     st.error("AI detected abnormal machine behavior!")

#     st.dataframe(
#         anomaly_df[
#             [
#                 'machine_id',
#                 'temperature',
#                 'vibration',
#                 'pressure',
#                 'rpm',
#                 'power_usage',
#                 'anomaly'
#             ]
#         ],
#         use_container_width=True
#     )

# else:
#     st.success("No AI anomalies detected.")

# # ==========================================
# # MACHINE STATUS OVERVIEW
# # ==========================================

# st.subheader("🛠 Machine Status Overview")

# c1, c2, c3 = st.columns(3)

# c1.success(f"🟢 NORMAL: {normal_count}")
# c2.warning(f"🟡 WARNING: {warning_count}")
# c3.error(f"🔴 CRITICAL: {critical_count}")

# st.markdown("---")

# # ==========================================
# # LIVE TELEMETRY TABLE
# # ==========================================

# with st.expander("📡 View Live Machine Telemetry"):

#     st.dataframe(
#         df.head(150),
#         width="stretch"
#     )
# st.subheader("💚 Machine Health Scores")

# health_df = (
#     df.sort_values(by='timestamp', ascending=False)
#       .drop_duplicates(subset='machine_id')
# )

# health_df = health_df[
#     ['machine_id', 'machine_type', 'health_score', 'state']
# ].sort_values(by='health_score')

# display_df = df[
#     [
#         'machine_id',
#         'machine_type',
#         'state',
#         'temperature',
#         'vibration',
#         'pressure',
#         'rpm',
#         'power_usage',
#         'health_score',
#         'timestamp',
#         'failure_percentage',
#         'risk_level',
#         'anomaly'
#     ]
# ]

# display_df = display_df.sort_values(
#     by='failure_percentage',
#     ascending=False
# )

# st.dataframe(
#     display_df.head(50),
#     use_container_width=True
# )

# health_chart = px.bar(
#     health_df,
#     x='machine_id',
#     y='health_score',
#     color='health_score',
#     title='Machine Health Score Analysis',
#     text='health_score'
# )

# health_chart.update_layout(
#     xaxis_title="Machine ID",
#     yaxis_title="Health Score",
# )

# st.plotly_chart(
#     health_chart,
#     use_container_width=True
# )

# # ==========================================
# # MACHINE HEALTH DISTRIBUTION
# # ==========================================

# state_counts = df['state'].value_counts().reset_index()
# state_counts.columns = ['State', 'Count']

# fig1 = px.pie(
#     state_counts,
#     names='State',
#     values='Count',
#     title='Machine Health Distribution'
# )

# st.plotly_chart(fig1, use_container_width=True)

# # ==========================================
# # TEMPERATURE MONITORING
# # ==========================================

# st.subheader("🌡 Temperature Monitoring")

# fig2 = px.line(
#     df,
#     x='timestamp',
#     y='temperature',
#     color='machine_id',
#     title='Temperature Trends',
#     markers=True
# )

# st.plotly_chart(fig2, use_container_width=True)

# # ==========================================
# # VIBRATION MONITORING
# # ==========================================

# st.subheader("📈 Vibration Monitoring")

# fig3 = px.line(
#     df,
#     x='timestamp',
#     y='vibration',
#     color='machine_id',
#     title='Vibration Trends',
#     markers=True
# )

# st.plotly_chart(fig3, use_container_width=True)

# # ==========================================
# # POWER USAGE MONITORING
# # ==========================================

# st.subheader("⚡ Power Consumption Monitoring")

# fig4 = px.area(
#     df,
#     x='timestamp',
#     y='power_usage',
#     color='machine_id',
#     title='Power Usage Trends'
# )

# st.plotly_chart(fig4, use_container_width=True)

# # ==========================================
# # MACHINE FILTER
# # ==========================================

# st.sidebar.header("🔍 Machine Filter")

# selected_machine = st.sidebar.selectbox(
#     "Select Machine ID",
#     options=["All"] + list(df['machine_id'].unique())
# )

# if selected_machine != "All":
#     filtered_df = df[df['machine_id'] == selected_machine]

#     st.subheader(f"🖥 Detailed Analytics for {selected_machine}")

#     st.dataframe(filtered_df, use_container_width=True)

# # ==========================================
# # CRITICAL MACHINE ALERTS
# # ==========================================

# critical_df = df[df['state'] == 'CRITICAL']

# st.subheader("🚨 Critical Machine Alerts")

# if len(critical_df) > 0:
#     st.error("Critical machines detected!")

#     st.dataframe(
#         critical_df,
#         use_container_width=True
#     )

# else:
#     st.success("No critical machines currently.")

# # ==========================================
# # FOOTER
# # ==========================================

# st.markdown("---")

# st.caption("⚙ Real-Time Industrial Telemetry Monitoring System")

# connection.close()

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

# ==========================================
# HEALTH SCORE FUNCTION
# ==========================================

def calculate_health(row):

    score = 100

    if row['temperature'] > 100:
        score -= 50
    elif row['temperature'] > 85:
        score -= 30
    elif row['temperature'] > 70:
        score -= 10

    if row['vibration'] > 1.0:
        score -= 30
    elif row['vibration'] > 0.7:
        score -= 20
    elif row['vibration'] > 0.4:
        score -= 10

    if row['pressure'] < 20:
        score -= 15

    if row['rpm'] < 700:
        score -= 10

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

st.markdown("""

<style>

/* Main Background */
.stApp {
    background-color: #050816;
    color: white;
}

/* Metric Cards */
[data-testid="metric-container"] {

    background: linear-gradient(
        145deg,
        #0f172a,
        #111827
    );

    border: 1px solid #1e293b;

    padding: 15px;

    border-radius: 15px;

    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {

    background-color: #111827;
}

/* Tables */
[data-testid="stDataFrame"] {

    border-radius: 12px;

    overflow: hidden;
}

/* Headers */
h1, h2, h3 {

    color: #f8fafc;
}

/* Alert Boxes */
.stAlert {

    border-radius: 12px;
}

</style>

""", unsafe_allow_html=True)

st_autorefresh(
    interval=5000,
    key="telemetryrefresh"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏭 Industrial Telemetry Monitoring Dashboard")
st.success(
    "🟢 SYSTEM STATUS: ALL PIPELINES OPERATIONAL"
)

st.caption(
    f"🕒 Last Updated: "
    f"{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
st.info(
    f"⚡ Live Monitoring Active | "
    f"{pd.Timestamp.now().strftime('%H:%M:%S')}"
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
# LOAD AI MODEL
# ==========================================

MODEL_PATH = os.path.join(
    "ai-models",
    "predictive_maintenance_model.pkl"
)

predictive_model = joblib.load(MODEL_PATH)

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

# Fill None with 'Unknown'
df['machine_category'] = df['machine_category'].fillna('Unknown')

# ==========================================
# CATEGORY FILTER
# ==========================================

st.sidebar.header("🏭 Machine Category Filter")

categories = sorted(

    [
        category
        for category in df["machine_category"].unique()
        if category not in [None, "None"]
    ]

)

selected_category = st.sidebar.selectbox(

    "Select Machine Category",

    ["All"] + list(categories)

)

if selected_category != "All":

    filtered_df = df[
        df["machine_category"] == selected_category
    ]

else:

    filtered_df = df.copy()



st.sidebar.header("🔍 Machine Filter")

selected_machine = st.sidebar.selectbox(

    "Select Machine ID",

    ["All"] + list(
        filtered_df['machine_id'].unique()
    )

)

if selected_machine != "All":

    filtered_df = filtered_df[
        filtered_df['machine_id'] == selected_machine
    ]

if filtered_df.empty:

    st.warning("No telemetry data available.")

    st.stop()

# ==========================================
# TIMESTAMP + HEALTH SCORE
# ==========================================

filtered_df['timestamp'] = pd.to_datetime(
    filtered_df['timestamp']
)

filtered_df['health_score'] = filtered_df.apply(
    calculate_health,
    axis=1
)

# ==========================================
# FAILURE PREDICTION
# ==========================================

# ==========================================
# FAILURE PREDICTION
# ==========================================

prediction_features = filtered_df[

    [

        'temperature',

        'vibration',

        'rpm',

        'pressure',

        'power_usage'

    ]

].copy()

# ==========================================
# MAP OLD TELEMETRY TO ML MODEL FEATURES
# ==========================================

prediction_features.columns = [

    'Air temperature [K]',

    'Process temperature [K]',

    'Rotational speed [rpm]',

    'Torque [Nm]',

    'Tool wear [min]'

]

# ==========================================
# AI PREDICTION
# ==========================================

filtered_df['failure_probability'] = (

    predictive_model.predict_proba(

        prediction_features

    )[:, 1]

)

filtered_df['failure_percentage'] = (

    filtered_df['failure_probability'] * 100

).round(2)

# ==========================================
# EXECUTIVE COMMAND CENTER
# ==========================================

st.markdown("---")

st.subheader(
    "🏭 Executive Operations Command Center"
)

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_machines = filtered_df["machine_id"].nunique()

critical_alerts = len(

    filtered_df[
        filtered_df["health_score"] < 40
    ]

)

average_health = round(

    filtered_df["health_score"].mean(),

    2

)

active_anomalies = len(

    filtered_df[
        filtered_df["health_score"] < 60
    ]

)

system_stability = max(

    round(
        100 - active_anomalies * 2,
        2
    ),

    0

)

# ==========================================
# KPI DISPLAY
# ==========================================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    "Machines Online",
    total_machines
)

kpi2.metric(
    "Critical Alerts",
    critical_alerts
)

kpi3.metric(
    "Avg Health Score",
    f"{average_health}%"
)

kpi4.metric(
    "Active Anomalies",
    active_anomalies
)

kpi5.metric(
    "System Stability",
    f"{system_stability}%"
)

# ==========================================
# RISK LEVEL
# ==========================================

def risk_level(prob):

    if prob >= 90:
        return "🔴 CRITICAL"

    elif prob >= 70:
        return "🟡 HIGH"

    elif prob >= 40:
        return "🟢 MODERATE"

    return "✅ LOW"

filtered_df['risk_level'] = filtered_df[
    'failure_percentage'
].apply(risk_level)

# ==========================================
# ANOMALY DETECTION
# ==========================================

features = filtered_df[
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

filtered_df['anomaly'] = anomaly_model.fit_predict(
    features
)

filtered_df['anomaly'] = filtered_df[
    'anomaly'
].map({
    1: 'NORMAL',
    -1: 'ANOMALY'
})

# ==========================================
# KPI METRICS
# ==========================================

total_machines = filtered_df[
    'machine_id'
].nunique()

critical_count = len(
    filtered_df[
        filtered_df['state'] == 'CRITICAL'
    ]
)

warning_count = len(
    filtered_df[
        filtered_df['state'] == 'WARNING'
    ]
)

normal_count = len(
    filtered_df[
        filtered_df['state'] == 'NORMAL'
    ]
)

avg_temp = round(
    filtered_df['temperature'].mean(),
    2
)

avg_vibration = round(
    filtered_df['vibration'].mean(),
    2
)

high_risk_count = len(
    filtered_df[
        filtered_df['failure_probability'] > 0.7
    ]
)

ai_anomalies = len(
    filtered_df[
        filtered_df['anomaly'] == 'ANOMALY'
    ]
)

highest_risk = round(
    filtered_df['failure_percentage'].max(),
    2
)


# ==========================================
# KPI DISPLAY
# ==========================================

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("🏭 Machines", total_machines)
col2.metric("🚨 Critical", critical_count)
col3.metric("🟡 Warning", warning_count)
col4.metric("🌡 Avg Temp", avg_temp)
col5.metric("📈 Avg Vib", avg_vibration)
col6.metric("🤖 AI Anomalies", ai_anomalies)
col7.metric("🔥 Highest Risk", f"{highest_risk}%")

st.markdown("---")

# ==========================================
# LIVE ALERT PANEL
# ==========================================

st.subheader("🚨 Live Factory Alerts")

alerts_df = filtered_df[

    (filtered_df['state'] == 'WARNING') |

    (filtered_df['state'] == 'CRITICAL')

]

alerts_df = alerts_df.sort_values(
    by='timestamp',
    ascending=False
)

if len(alerts_df) > 0:

    st.warning(
        f"{len(alerts_df)} active machine alerts detected!"
    )

    st.dataframe(

        alerts_df[
            [
                'machine_id',
                'machine_category',
                'state',
                'temperature',
                'vibration',
                'pressure',
                'failure_percentage',
                'risk_level'
            ]
        ],

        use_container_width=True

    )

else:

    st.success(
        "No active alerts detected."
    )

# ==========================================
# AI RISK MAP
# ==========================================

st.subheader("🔥 Live System Risk Overview")

risk_chart = px.scatter(

    filtered_df,

    x='temperature',

    y='vibration',

    size='failure_percentage',

    color='risk_level',

    hover_data=[
        'machine_id',
        'machine_category'
    ],

    title='AI Risk Intelligence Map'

)

st.plotly_chart(
    risk_chart,
    use_container_width=True
)

# ==========================================
# PREDICTIVE MAINTENANCE
# ==========================================

st.subheader("🤖 Predictive Maintenance Intelligence")

high_risk_df = filtered_df[
    filtered_df['failure_probability'] > 0.7
]

prediction_table = high_risk_df[
    [
        'machine_id',
        'machine_category',
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

st.dataframe(
    prediction_table.head(10),
    use_container_width=True
)

# ==========================================
# ANOMALY TABLE
# ==========================================

st.subheader("🤖 AI Detected Machine Anomalies")

anomaly_df = filtered_df[
    filtered_df['anomaly'] == 'ANOMALY'
]

if len(anomaly_df) > 0:

    st.error(
        "AI detected abnormal machine behavior!"
    )

    st.dataframe(

        anomaly_df[
            [
                'machine_id',
                'machine_category',
                'temperature',
                'vibration',
                'pressure',
                'rpm',
                'power_usage'
            ]
        ],

        use_container_width=True
    )

else:

    st.success("No AI anomalies detected.")

# ==========================================
# TELEMETRY TABLE
# ==========================================

st.subheader("📡 Live Machine Telemetry")

st.dataframe(
    filtered_df.head(50),
    use_container_width=True
)

# ==========================================
# HEALTH SCORES
# ==========================================

st.subheader("🎰 Machine Health Scores")

health_df = (

    filtered_df
    .sort_values(
        by='timestamp',
        ascending=False
    )
    .drop_duplicates(
        subset='machine_id'
    )

)

health_chart = px.bar(

    health_df,

    x='machine_id',

    y='health_score',

    color='health_score',

    title='Machine Health Score Analysis',

    text='health_score'

)

st.plotly_chart(
    health_chart,
    use_container_width=True
)

# ==========================================
# MACHINE STATE DISTRIBUTION
# ==========================================

state_counts = filtered_df[
    'state'
].value_counts().reset_index()

state_counts.columns = [
    'State',
    'Count'
]

fig1 = px.pie(

    state_counts,

    names='State',

    values='Count',

    title='Machine Health Distribution'

)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# TEMPERATURE TREND
# ==========================================

st.subheader("🌡 Temperature Monitoring")

fig2 = px.line(

    filtered_df,

    x='timestamp',

    y='temperature',

    color='machine_id',

    title='Temperature Trends',

    markers=True

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# VIBRATION TREND
# ==========================================

st.subheader("📈 Vibration Monitoring")

fig3 = px.line(

    filtered_df,

    x='timestamp',

    y='vibration',

    color='machine_id',

    title='Vibration Trends',

    markers=True

)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# POWER TREND
# ==========================================

st.subheader("⚡ Power Consumption Monitoring")

fig4 = px.area(

    filtered_df,

    x='timestamp',

    y='power_usage',

    color='machine_id',

    title='Power Usage Trends'

)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# CRITICAL ALERTS
# ==========================================

critical_df = filtered_df[

    (filtered_df['state'] == 'CRITICAL') |

    (filtered_df['risk_level'] == '🔴 CRITICAL')

]

st.subheader("🚨 Critical Machine Alerts")

if len(critical_df) > 0:

    st.error(
    "🚨 CRITICAL INDUSTRIAL FAILURE RISK DETECTED 🚨"
)

    st.dataframe(
        critical_df,
        use_container_width=True
    )

else:

    st.success(
        "No critical machines currently."
    )
# ==========================================
# SIDEBAR SYSTEM STATUS
# ==========================================

st.sidebar.markdown("---")

st.sidebar.success(
    "🟢 Kafka Streaming Active"
)

st.sidebar.success(
    "🟢 PostgreSQL Connected"
)

st.sidebar.success(
    "🟢 AI Prediction Engine Running"
)

st.sidebar.success(
    "🟢 Live Telemetry Active"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "⚙ Real-Time Industrial Telemetry Monitoring System"
)

connection.close()