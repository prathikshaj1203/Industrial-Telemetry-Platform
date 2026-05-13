# 🏭 Industrial Telemetry Platform

## Real-Time Industrial Monitoring & Predictive Maintenance System

An AI-powered industrial telemetry platform that simulates smart factory monitoring using real-time telemetry streaming, AI-based predictive maintenance, anomaly detection, and industrial dashboards.

---

# 🚀 Features

* Real-time machine telemetry streaming
* AI predictive maintenance
* AI anomaly detection
* Live industrial monitoring dashboard
* Machine health scoring
* Grafana monitoring & alerts
* Kafka-based streaming pipeline
* PostgreSQL telemetry storage

---

# 🏭 Simulated Machines

* WLD_101 — Welding Machine
* CNC_303 — CNC Machine
* HYD_404 — Hydraulic Machine
* PNT_505 — Paint Shop Machine
* CNV_202 — Conveyor System

---

# 🧠 AI Models

## Predictive Maintenance

* Model: Random Forest Classifier
* Predicts machine failure probability
* Generates AI-based risk levels

## Anomaly Detection

* Model: Isolation Forest
* Detects abnormal machine behavior

---

# 📊 Dashboard Modules

* Live telemetry monitoring
* Predictive maintenance intelligence
* AI anomaly detection
* Machine health analysis
* Temperature monitoring
* Vibration monitoring
* Power consumption analysis
* Critical machine alerts

---

# 🏗️ System Architecture

```text
Industrial Machines
        ↓
Kafka Producer
        ↓
Apache Kafka
        ↓
Kafka Consumer
        ↓
PostgreSQL Database
        ↓
AI Models
        ↓
Streamlit Dashboard
        ↓
Grafana Alerts
```

---

# ⚙️ Tech Stack

* Python
* Streamlit
* PostgreSQL
* Apache Kafka
* Grafana
* Docker
* Scikit-learn
* Pandas
* Plotly

---

# 📁 Project Structure

```text
industrial-telemetry-platform/
│
├── ai-models/
├── dashboard/
├── kafka-streaming/
├── screenshots/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🔐 Environment Variables

```env
DB_HOST=localhost
DB_NAME=telemetry_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

---

# ▶️ Run Project

```bash
# Start Docker Services
docker compose up -d

# Run Kafka Producer
python producer.py

# Run Kafka Consumer
python consumer.py

# Train AI Model
python predictive_maintenance.py

# Launch Dashboard
streamlit run dashboard.py
```

---

# 📈 Future Enhancements

* Expanded factory machine ecosystem
* AI-assisted machine inspection
* Manual diagnostic workflows
* Image upload for inspection evidence
* Cloud deployment
* Full Docker orchestration

---

# 👨‍💻 Author

Prathiksha J
