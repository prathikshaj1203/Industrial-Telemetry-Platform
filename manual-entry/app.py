import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import joblib
import os
import time

from dotenv import load_dotenv
from datetime import datetime

from machine_components import machine_components
from machine_questions import machine_questions
from maintenance_actions import maintenance_actions

# ======================================
# LOAD ENV
# ======================================

load_dotenv()

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(

    page_title="AI Industrial Diagnostic Assistant",

    layout="wide"

)

# ======================================
# DATABASE CONNECTION
# ======================================

connection = psycopg2.connect(

    host=os.getenv("DB_HOST"),

    database=os.getenv("DB_NAME"),

    user=os.getenv("DB_USER"),

    password=os.getenv("DB_PASSWORD"),

    port=os.getenv("DB_PORT")

)

cursor = connection.cursor()

# ======================================
# LOAD MODEL
# ======================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(

    BASE_DIR,

    "..",

    "ai-models",

    "predictive_maintenance_model.pkl"

)

predictive_model = joblib.load(MODEL_PATH)

# ======================================
# CUSTOM CSS
# ======================================

st.markdown("""

<style>

.stApp {

    background-color: #050816;

    color: white;

}

[data-testid="metric-container"] {

    background: linear-gradient(
        145deg,
        #0f172a,
        #111827
    );

    border: 1px solid #1e293b;

    padding: 15px;

    border-radius: 15px;
}

section[data-testid="stSidebar"] {

    background-color: #111827;
}

</style>

""", unsafe_allow_html=True)

# ======================================
# TITLE
# ======================================

st.title(
    "🧠 AI Industrial Diagnostic Assistant"
)

st.caption(
    "Hybrid Predictive Maintenance & Failure Intelligence System"
)

st.success(
    "🟢 AI Predictive Maintenance Engine Active"
)

# ======================================
# SIDEBAR
# ======================================

st.sidebar.header(
    "🏭 Machine Selection"
)

categories = list(
    machine_components.keys()
)

selected_category = st.sidebar.selectbox(

    "Select Machine Category",

    categories

)

monitoring_type = st.sidebar.selectbox(

    "Select Monitoring Mode",

    [

        "Sensor-Based",

        "Manual Inspection"

    ]

)

# ======================================
# MACHINE DATA
# ======================================

machine_data = machine_components[
    selected_category
]

machine_type = machine_data[
    "machine_type"
]

components = machine_data[
    "components"
]

# ======================================
# COMPONENT DISPLAY
# ======================================

st.markdown("## 🔩 Machine Components")

component_cols = st.columns(3)

for index, component in enumerate(components):

    component_cols[index % 3].info(component)

# ======================================
# QUESTION ENGINE
# ======================================

answers = {}

if monitoring_type == "Manual Inspection":

    st.markdown("---")

    st.subheader(
        "📝 AI Diagnostic Questionnaire"
    )

    questions = machine_questions[
        selected_category
    ]

    for item in questions:

        question = item["question"]

        options = item["options"]

        answers[question] = st.selectbox(

            question,

            options,

            key=question

        )

# ======================================
# SENSOR INPUTS
# ======================================

if monitoring_type == "Sensor-Based":

    st.markdown("---")

    st.subheader(
        "📡 Machine Telemetry Inputs"
    )

    col1, col2 = st.columns(2)

    with col1:

        air_temperature = st.slider(

            "Air Temperature [K]",

            290.0,
            320.0,

            300.0

        )

        process_temperature = st.slider(

            "Process Temperature [K]",

            300.0,
            340.0,

            310.0

        )

        rotational_speed = st.slider(

            "Rotational Speed [rpm]",

            1000,
            3000,

            1500

        )

    with col2:

        torque = st.slider(

            "Torque [Nm]",

            0.0,
            80.0,

            40.0

        )

        tool_wear = st.slider(

            "Tool Wear [min]",

            0,
            300,

            50

        )

# ======================================
# IMAGE UPLOAD
# ======================================

st.markdown("---")

st.subheader(
    "📷 Machine Inspection Image"
)

uploaded_file = st.file_uploader(

    "Upload machine image for future AI vision analysis",

    type=["jpg", "jpeg", "png"]

)

if uploaded_file:

    st.image(
        uploaded_file,
        use_container_width=True
    )

# ======================================
# RUN BUTTON
# ======================================

st.markdown("---")

run_prediction = st.button(
    "🚀 Run AI Failure Diagnosis"
)

# ======================================
# AI ENGINE
# ======================================

if run_prediction:

    # ==================================
    # MANUAL FEATURE ENGINEERING
    # ==================================

    if monitoring_type == "Manual Inspection":

        air_temperature = 300
        process_temperature = 310
        rotational_speed = 1500
        torque = 40
        tool_wear = 50

        for question, answer in answers.items():

            if "Cooling" in question:

                if answer == "Average":
                    process_temperature += 10

                elif answer == "Poor":
                    process_temperature += 20

            if "Vibration" in question:

                if answer == "Medium":
                    rotational_speed += 300

                elif answer == "High":
                    rotational_speed += 600

                elif answer == "Severe":
                    rotational_speed += 900

            if "Oil leakage" in question:

                if answer == "Yes":
                    torque += 15

            if "alignment" in question.lower():

                if answer == "Misaligned":
                    rotational_speed += 500

            if "Motor" in question:

                if answer == "Failing":
                    torque += 20

                elif answer == "Critical":
                    torque += 30

    # ==================================
    # MODEL FEATURES
    # ==================================

    features = np.array([[

        air_temperature,

        process_temperature,

        rotational_speed,

        torque,

        tool_wear

    ]])

    # ==================================
    # PREDICTION
    # ==================================

    prediction_probability = predictive_model.predict_proba(
        features
    )[0][1]

    failure_probability = round(

        prediction_probability * 100,

        2

    )

    # ==================================
    # HEALTH SCORE
    # ==================================

    health_score = 100 - failure_probability

    if tool_wear > 200:
        health_score -= 15

    if torque > 60:
        health_score -= 10

    if process_temperature > 325:
        health_score -= 10

    health_score = max(
        round(health_score, 2),
        0
    )

    # ==================================
    # RISK LEVEL
    # ==================================

    if failure_probability >= 80:

        risk_level = "🔴 CRITICAL"

    elif failure_probability >= 60:

        risk_level = "🟡 HIGH"

    elif failure_probability >= 40:

        risk_level = "🟠 MODERATE"

    else:

        risk_level = "🟢 LOW"

    # ==================================
    # RUL
    # ==================================

    wear_factor = tool_wear * 0.4

    torque_factor = torque * 1.2

    temperature_factor = (

        process_temperature - 300

    ) * 1.5

    rpm_factor = (

        rotational_speed / 100

    )

    total_degradation = (

        wear_factor +

        torque_factor +

        temperature_factor +

        rpm_factor

    )

    remaining_useful_life = max(

        round(

            300 - total_degradation,

            2

        ),

        5

    )

    # ==================================
    # COMPONENT PREDICTION
    # ==================================

    if tool_wear > 220:

        failed_component = "Welding Tip"

    elif torque > 65:

        failed_component = "Servo Motor"

    elif process_temperature > 325:

        failed_component = "Cooling Unit"

    elif rotational_speed > 2500:

        failed_component = "Joint Actuator"

    elif air_temperature > 315:

        failed_component = "Power Supply"

    else:

        failed_component = "Servo Motor"

    # ==================================
    # MAINTENANCE DATA
    # ==================================

    maintenance_data = maintenance_actions.get(

        failed_component,

        {

            "issue":
            "General degradation detected.",

            "severity":
            "MODERATE",

            "downtime":
            "Unknown",

            "recovery": [

                "Perform diagnostics",

                "Inspect components"

            ]

        }

    )

        # ==================================
    # ANOMALY DETECTION ENGINE
    # ==================================

    anomaly_score = 0

    # ==================================
    # TEMPERATURE ANOMALY
    # ==================================

    if process_temperature > 325:

        anomaly_score += 30

    elif process_temperature > 318:

        anomaly_score += 15

    # ==================================
    # TORQUE ANOMALY
    # ==================================

    if torque > 70:

        anomaly_score += 30

    elif torque > 55:

        anomaly_score += 15

    # ==================================
    # TOOL WEAR ANOMALY
    # ==================================

    if tool_wear > 250:

        anomaly_score += 25

    elif tool_wear > 180:

        anomaly_score += 10

    # ==================================
    # RPM ANOMALY
    # ==================================

    if rotational_speed > 2700:

        anomaly_score += 20

    elif rotational_speed > 2200:

        anomaly_score += 10

    # ==================================
    # FINAL CLASSIFICATION
    # ==================================

    if anomaly_score >= 70:

        anomaly_level = "🔴 Severe Anomaly"

    elif anomaly_score >= 40:

        anomaly_level = "🟠 Moderate Anomaly"

    elif anomaly_score >= 20:

        anomaly_level = "🟡 Mild Anomaly"

    else:

        anomaly_level = "🟢 Normal"

    # ==================================
    # FEATURE IMPORTANCE
    # ==================================

    feature_importance = {

        "Air Temperature":
        air_temperature / 320,

        "Process Temperature":
        process_temperature / 340,

        "Rotational Speed":
        rotational_speed / 3000,

        "Torque":
        torque / 80,

        "Tool Wear":
        tool_wear / 300

    }

    # ==================================
    # SAVE HISTORY
    # ==================================

    cursor.execute(

        """

        INSERT INTO machine_diagnosis_history (

            machine_type,
            category,
            monitoring_type,
            temperature,
            vibration,
            pressure,
            rpm,
            power_usage,
            failure_probability,
            health_score,
            risk_level,
            failed_component,
            estimated_failure,
            timestamp

        )

        VALUES (

            %s, %s, %s, %s, %s, %s,

            %s, %s, %s, %s, %s,

            %s, %s, %s

        )

        """,

        (

            machine_type,

            selected_category,

            monitoring_type,

            float(air_temperature),

            float(process_temperature),

            float(torque),

            float(rotational_speed),

            float(tool_wear),

            float(failure_probability),

            float(health_score),

            risk_level,

            failed_component,

            f"{remaining_useful_life} Hours",

            datetime.now()

        )

    )

    connection.commit()

    # ==================================
    # RESULTS
    # ==================================

    st.markdown("---")

    st.header(
        "🤖 AI Failure Prediction Results"
    )
        # ==================================
    # REAL-TIME ALERT ENGINE
    # ==================================

    active_alerts = []

    if process_temperature > 330:

        active_alerts.append({

            "level": "CRITICAL",

            "message":
            "Extreme process temperature detected"

        })

    elif process_temperature > 320:

        active_alerts.append({

            "level": "WARNING",

            "message":
            "Elevated process temperature"

        })

    if torque > 70:

        active_alerts.append({

            "level": "CRITICAL",

            "message":
            "Torque overload detected"

        })

    elif torque > 60:

        active_alerts.append({

            "level": "WARNING",

            "message":
            "Torque instability observed"

        })
    # ==================================
    # LIVE ALERT DISPLAY
    # ==================================

    if len(active_alerts) > 0:

        st.subheader("🚨 Live Industrial Alerts")

        for alert in active_alerts:

            if alert["level"] == "CRITICAL":

                st.error(

                    f"🚨 {alert['message']}"

                )

            else:

                st.warning(

                    f"⚠ {alert['message']}"

                )

    else:

        st.success(
            "✅ No active industrial alerts"
        )

    metric1, metric2, metric3, metric4, metric5 = st.columns(5)

    metric1.metric(
        "Risk Level",
        risk_level
    )

    metric2.metric(
        "Failure Probability",
        f"{failure_probability}%"
    )

    metric3.metric(
        "Machine Health",
        f"{health_score}%"
    )

    metric4.metric(
        "Remaining Useful Life",
        f"{remaining_useful_life} Hours"
    )

    metric5.metric(

        "Anomaly Status",

        anomaly_level

    )
    # ==================================
    # DIGITAL TWIN STATUS PANEL
    # ==================================

    st.subheader("🧩 Digital Twin Machine Status")

    twin_cols = st.columns(3)

    component_status = {}

    for component in components:

        component_status[component] = "Healthy"

    component_status[failed_component] = "Critical"

    for index, component in enumerate(components):

        status = component_status[component]

        with twin_cols[index % 3]:

            if status == "Critical":

                st.error(

                    f"""

                    🔴 {component}

                    Status: Critical

                    """

                )

            else:

                st.success(

                    f"""

                    🟢 {component}

                    Status: Healthy

                    """

                )

    # ==================================
    # COMPONENT ALERT
    # ==================================

    st.error(
        f"⚠ Likely Faulty Component: {failed_component}"
    )

    # ==================================
    # ROOT CAUSE
    # ==================================

    st.subheader(
        "🔍 Root Cause Analysis"
    )

    st.warning(
        maintenance_data["issue"]
    )

    # ==================================
    # RECOVERY
    # ==================================

    st.subheader(
        "🛠 Recovery Actions"
    )

    for action in maintenance_data["recovery"]:

        st.success(
            f"✔ {action}"
        )

    # ==================================
    # DOWNTIME
    # ==================================
        # ==================================
    # PREDICTIVE MAINTENANCE SCHEDULER
    # ==================================

    st.subheader(
        "📅 Predictive Maintenance Scheduler"
    )

    if remaining_useful_life <= 24:

        maintenance_priority = "🔴 Immediate"

        maintenance_window = "Within 6 Hours"

        shutdown_status = "Emergency shutdown recommended"

    elif remaining_useful_life <= 72:

        maintenance_priority = "🟠 High"

        maintenance_window = "Within 24 Hours"

        shutdown_status = "Controlled maintenance required"

    elif remaining_useful_life <= 150:

        maintenance_priority = "🟡 Medium"

        maintenance_window = "Within 3 Days"

        shutdown_status = "Inspection scheduling recommended"

    else:

        maintenance_priority = "🟢 Low"

        maintenance_window = "Within 7 Days"

        shutdown_status = "Routine monitoring sufficient"

    sched1, sched2, sched3 = st.columns(3)

    sched1.metric(

        "Maintenance Priority",

        maintenance_priority

    )

    sched2.metric(

        "Recommended Window",

        maintenance_window

    )

    sched3.metric(

        "Operational Status",

        shutdown_status

    )
    st.subheader(
        "⏳ Estimated Downtime"
    )

    st.info(
        maintenance_data["downtime"]
    )

    # ==================================
    # FAILURE GAUGE
    # ==================================

    st.subheader(
        "🎯 AI Failure Probability Meter"
    )

    gauge_chart = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=failure_probability,

            title={
                'text': "Failure Probability %"
            },

            gauge={

                'axis': {
                    'range': [0, 100]
                },

                'steps': [

                    {
                        'range': [0, 40],
                        'color': "green"
                    },

                    {
                        'range': [40, 70],
                        'color': "yellow"
                    },

                    {
                        'range': [70, 100],
                        'color': "red"
                    }

                ]

            }

        )

    )

    st.plotly_chart(

        gauge_chart,

        use_container_width=True,

        key="failure_gauge"

    )

    # ==================================
    # HEALTH RING
    # ==================================

    st.subheader(
        "💚 Machine Health Ring"
    )

    health_ring = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=health_score,

            title={
                'text': "Machine Health %"
            },

            gauge={

                'axis': {
                    'range': [0, 100]
                }

            }

        )

    )

    st.plotly_chart(

        health_ring,

        use_container_width=True,

        key="health_ring"

    )

    # ==================================
    # FEATURE IMPORTANCE
    # ==================================

    st.subheader(
        "🧠 AI Feature Importance Analysis"
    )

    importance_df = pd.DataFrame({

        "Feature": feature_importance.keys(),

        "Impact": feature_importance.values()

    })

    importance_chart = px.bar(

        importance_df,

        x="Feature",

        y="Impact",

        color="Impact",

        text="Impact",

        title="Feature Contribution Analysis"

    )

    st.plotly_chart(

        importance_chart,

        use_container_width=True

    )

# ======================================
# HISTORY DASHBOARD
# ======================================

st.markdown("---")

st.header(
    "📜 Diagnosis History Dashboard"
)

history_query = """

SELECT *

FROM machine_diagnosis_history

ORDER BY timestamp DESC

LIMIT 20

"""

history_df = pd.read_sql(

    history_query,

    connection

)

if len(history_df) > 0:

    st.dataframe(

        history_df,

        use_container_width=True

    )
# ======================================
# LIVE TELEMETRY STREAM
# ======================================

st.markdown("---")

st.header("📡 Live Telemetry Streaming")



start_stream = st.checkbox(
    "Enable Live Telemetry Simulation"
)

if start_stream and not run_prediction:

    st.warning(
        "Run AI diagnosis before starting telemetry stream."
    )

if start_stream and run_prediction:

    telemetry_placeholder = st.empty()

    chart_placeholder = st.empty()

    telemetry_history = []

    for i in range(20):

        simulated_temperature = round(

            np.random.normal(
                process_temperature,
                2
            ),

            2

        )

        simulated_torque = round(

            np.random.normal(
                torque,
                1.5
            ),

            2

        )

        simulated_rpm = round(

            np.random.normal(
                rotational_speed,
                50
            ),

            2

        )

        telemetry_history.append({

            "Time": i,

            "Temperature": simulated_temperature,

            "Torque": simulated_torque,

            "RPM": simulated_rpm

        })

        live_df = pd.DataFrame(
            telemetry_history
        )

        telemetry_placeholder.dataframe(

            live_df.tail(5),

            use_container_width=True

        )

        live_chart = px.line(

            live_df,

            x="Time",

            y=[

                "Temperature",

                "Torque",

                "RPM"

            ],

            title="Real-Time Telemetry Feed"

        )

        live_chart.update_layout(

            paper_bgcolor="#050816",

            plot_bgcolor="#050816",

            font=dict(color="white")

        )

        chart_placeholder.plotly_chart(

            live_chart,

            use_container_width=True,

            key=f"live_chart_{i}"

        )

        time.sleep(0.5)
# ======================================
# CLOSE DATABASE
# ======================================

connection.close()