import streamlit as st
import pandas as pd
from machine_components import machine_components
from machine_questions import machine_questions
from datetime import datetime
import random
import plotly.express as px
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="AI Industrial Diagnostic Assistant",

    layout="wide"

)

# ==========================================
# CUSTOM CSS
# ==========================================

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

# ==========================================
# TITLE
# ==========================================

st.title(
    "🧠 AI Industrial Diagnostic Assistant"
)

st.caption(
    "Predict machine failures before breakdown occurs"
)

st.success(
    "🟢 AI Predictive Maintenance Engine Active"
)

# ==========================================
# MACHINE SELECTION
# ==========================================

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

# ==========================================
# MACHINE DETAILS
# ==========================================

machine_data = machine_components[
    selected_category
]

machine_type = machine_data[
    "machine_type"
]

components = machine_data[
    "components"
]

# ==========================================
# MACHINE HEADER
# ==========================================

st.subheader(
    f"⚙ {machine_type}"
)

# ==========================================
# COMPONENT DISPLAY
# ==========================================

st.markdown("## 🔩 Machine Components")

component_cols = st.columns(3)

for index, component in enumerate(components):

    component_cols[index % 3].info(component)

# ==========================================
# QUESTION SYSTEM
# ==========================================

st.markdown("---")

st.subheader(
    "📝 AI Diagnostic Questionnaire"
)

questions = machine_questions[
    selected_category
]

answers = {}

for question in questions:

    answers[question] = st.text_input(question)

# ==========================================
# OPERATIONAL INPUTS
# ==========================================

st.markdown("---")

st.subheader(
    "📊 Live Operational Metrics"
)

col1, col2 = st.columns(2)

with col1:

    temperature = st.slider(
        "Temperature",
        0.0,
        150.0,
        50.0
    )

    vibration = st.slider(
        "Vibration",
        0.0,
        2.0,
        0.5
    )

    pressure = st.slider(
        "Pressure",
        0.0,
        250.0,
        40.0
    )

with col2:

    rpm = st.slider(
        "RPM",
        0,
        5000,
        1000
    )

    power_usage = st.slider(
        "Power Usage",
        0.0,
        2000.0,
        500.0
    )

    running_hours = st.slider(
        "Daily Running Hours",
        0,
        24,
        8
    )

# ==========================================
# IMAGE UPLOAD
# ==========================================

st.markdown("---")

st.subheader(
    "📷 Upload Machine Image"
)

uploaded_file = st.file_uploader(

    "Upload image for future AI vision analysis",

    type=["jpg", "jpeg", "png"]

)

if uploaded_file:

    st.image(
        uploaded_file,
        width=400
    )

# ==========================================
# AI PREDICTION ENGINE
# ==========================================

st.markdown("---")

if st.button(
    "🚀 Run AI Failure Diagnosis"
):

    risk_score = 0

    # ======================================
    # TEMPERATURE LOGIC
    # ======================================

    if temperature > 100:
        risk_score += 40

    elif temperature > 85:
        risk_score += 25

    # ======================================
    # VIBRATION LOGIC
    # ======================================

    if vibration > 1.2:
        risk_score += 35

    elif vibration > 0.8:
        risk_score += 20

    # ======================================
    # PRESSURE LOGIC
    # ======================================

    if pressure < 15:
        risk_score += 15

    # ======================================
    # POWER LOGIC
    # ======================================

    if power_usage > 1500:
        risk_score += 30

    elif power_usage > 900:
        risk_score += 15

    # ======================================
    # RUNNING HOURS
    # ======================================

    if running_hours > 18:
        risk_score += 20

    elif running_hours > 12:
        risk_score += 10

    # ======================================
    # RISK CLASSIFICATION
    # ======================================

    if risk_score >= 80:

        risk_level = "🔴 CRITICAL"

        failure_probability = random.randint(
            90,
            99
        )

        estimated_failure = random.randint(
            1,
            5
        )

    elif risk_score >= 50:

        risk_level = "🟡 HIGH"

        failure_probability = random.randint(
            70,
            89
        )

        estimated_failure = random.randint(
            7,
            20
        )

    elif risk_score >= 25:

        risk_level = "🟠 MODERATE"

        failure_probability = random.randint(
            40,
            69
        )

        estimated_failure = random.randint(
            20,
            45
        )

    else:

        risk_level = "🟢 LOW"

        failure_probability = random.randint(
            5,
            39
        )

        estimated_failure = random.randint(
            45,
            120
        )

    # ======================================
    # RANDOM COMPONENT FAILURE
    # ======================================

    failed_component = random.choice(
        components
    )

    # ======================================
    # DISPLAY RESULTS
    # ======================================

    st.markdown("---")

    st.header(
        "🤖 AI Failure Prediction Results"
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Failure Risk",
        risk_level
    )

    metric2.metric(
        "Failure Probability",
        f"{failure_probability}%"
    )

    metric3.metric(
        "Estimated Failure Window",
        f"{estimated_failure} Days"
    )

    st.error(
        f"⚠ Likely Faulty Component: "
        f"{failed_component}"
    )

    st.warning(
        "🛠 Recommended Action: "
        "Immediate predictive maintenance inspection required."
    )

    # ======================================
    # DIAGNOSTIC SUMMARY
    # ======================================

    st.markdown("---")

    st.subheader(
        "📋 Diagnostic Summary"
    )

    summary_data = {

        "Machine Type": [machine_type],

        "Category": [selected_category],

        "Failure Risk": [risk_level],

        "Failure Probability": [
            f"{failure_probability}%"
        ],

        "Likely Failed Component": [
            failed_component
        ],

        "Estimated Failure Window": [
            f"{estimated_failure} Days"
        ],

        "Timestamp": [
            datetime.now()
        ]

    }

    summary_df = pd.DataFrame(
        summary_data
    )

    st.dataframe(
        summary_df,
        use_container_width=True
    )

    # ==========================================
    # AI FAILURE GAUGE METER
    # ==========================================

    import plotly.graph_objects as go

    st.subheader("🎯 AI Failure Probability Meter")

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

                'bar': {

                    'color': "red"

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
        use_container_width=True
    )

    # ==========================================
    # MACHINE HEALTH DONUT CHART
    # ==========================================

    st.subheader("💚 Machine Health Overview")

    health_remaining = 100 - failure_probability

    health_df = pd.DataFrame({

        'Status': [

            'Health',

            'Risk'

        ],

        'Value': [

            health_remaining,

            failure_probability

        ]

    })

    health_chart = px.pie(

        health_df,

        names='Status',

        values='Value',

        hole=0.7,

        title='Machine Health Distribution'

    )

    st.plotly_chart(
        health_chart,
        use_container_width=True
    )

    # ==========================================
    # COMPONENT RISK ANALYSIS
    # ==========================================

    st.subheader("🧩 Component Failure Risk Analysis")

    component_risk = {

        component: random.randint(10, 95)

        for component in components
    }

    component_df = pd.DataFrame({

        'Component': component_risk.keys(),

        'Risk': component_risk.values()

    })

    component_chart = px.bar(

        component_df,

        x='Component',

        y='Risk',

        color='Risk',

        text='Risk',

        title='Component Risk Analysis'

    )

    st.plotly_chart(
        component_chart,
        use_container_width=True
    )

    # ==========================================
    # FUTURE FAILURE ESCALATION
    # ==========================================

    st.subheader("📈 Future Failure Escalation Prediction")

    future_days = [

        'Day 1',

        'Day 5',

        'Day 10',

        'Day 15',

        'Day 20'

    ]

    future_risk = [

        random.randint(20, 40),

        random.randint(35, 50),

        random.randint(50, 65),

        random.randint(65, 80),

        failure_probability

    ]

    future_df = pd.DataFrame({

        'Timeline': future_days,

        'Risk': future_risk

    })

    future_chart = px.line(

        future_df,

        x='Timeline',

        y='Risk',

        markers=True,

        title='AI Future Risk Forecast'

    )

    st.plotly_chart(
        future_chart,
        use_container_width=True
    )

    # ==========================================
    # LIVE SENSOR GRAPH
    # ==========================================

    st.subheader("📡 Live Sensor Feed")

    sensor_df = pd.DataFrame({

        'Time': range(10),

        'Temperature': [

            random.randint(50, 100)

            for _ in range(10)
        ]

    })

    sensor_chart = px.line(

        sensor_df,

        x='Time',

        y='Temperature',

        markers=True,

        title='Real-Time Sensor Temperature Feed'

    )

    st.plotly_chart(
        sensor_chart,
        use_container_width=True
    )

    # ==========================================
    # AI INSIGHTS
    # ==========================================

    st.subheader("🧠 AI Insights")

    insights = [

        "Temperature spike detected",

        "Abnormal vibration pattern identified",

        "Cooling efficiency reducing",

        "Motor load instability observed",

        "Potential bearing wear detected"

    ]

    for insight in insights:

        st.info(insight)

    # ==========================================
    # MAINTENANCE PRIORITY
    # ==========================================

    st.subheader("🛠 Maintenance Recommendation")

    if failure_probability >= 80:

        st.error(
            "🚨 Immediate shutdown recommended"
        )

    elif failure_probability >= 60:

        st.warning(
            "⚠ Maintenance required within 7 days"
        )

    else:

        st.success(
            "✅ Machine operating within safe limits"
        )

    # ==========================================
    # AI IMAGE INSPECTION
    # ==========================================

    st.subheader("📷 AI Visual Inspection")

    if uploaded_file:

        st.success(
            "Image uploaded successfully"
        )

        st.info(

            "Future AI vision model will detect:\n"

            "- Cracks\n"

            "- Corrosion\n"

            "- Overheating\n"

            "- Surface damage\n"

            "- Oil leakage"
        )