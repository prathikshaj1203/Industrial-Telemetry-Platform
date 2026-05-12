# Industrial Telemetry Platform

A real-time industrial telemetry and predictive monitoring platform built using Kafka, PostgreSQL, Docker, and Apache Airflow.

This project simulates industrial machine telemetry streams, validates incoming sensor data, stores clean telemetry into PostgreSQL, routes invalid events to a Dead Letter Queue (DLQ), and orchestrates workflows using Apache Airflow.

---

# Architecture

```text id="read1"
Industrial Machines
        ↓
Telemetry Producer
        ↓
Apache Kafka
        ↓
Validation Consumer
       ↙        ↘
Valid Data      Invalid Data
     ↓               ↓
PostgreSQL         DLQ
     ↓
Airflow Orchestration
```

---

# Tech Stack

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python         | Backend & Streaming Logic    |
| Apache Kafka   | Real-time Event Streaming    |
| PostgreSQL     | Telemetry Data Storage       |
| Docker         | Containerized Infrastructure |
| Apache Airflow | Workflow Orchestration       |
| JSON           | Telemetry Message Format     |

---

# Features

* Real-time industrial telemetry simulation
* Kafka-based event streaming pipeline
* Machine health state generation
* Sensor metric validation
* Dead Letter Queue (DLQ) handling
* PostgreSQL telemetry storage
* Dockerized infrastructure setup
* Airflow DAG orchestration
* Scalable streaming architecture

---

# Machine Metrics Simulated

* Temperature
* Vibration
* Pressure
* RPM
* Power Usage
* Machine State

---

# Project Structure

```text id="read2"
industrial-telemetry-platform/
│
├── kafka-streaming/
│   ├── producer.py
│   ├── consumer.py
│   ├── validated_consumer.py
│   ├── database_consumer.py
│   ├── dlq_consumer.py
│   ├── docker-compose.yml
│
├── airflow/
│   ├── dags/
│   │   └── telemetry_pipeline_dag.py
│   ├── logs/
│   ├── plugins/
│   └── docker-compose.yml
│
├── data_lake/
│
├── README.md
```

---

# Pipeline Flow

## 1. Telemetry Producer

Generates simulated industrial machine telemetry events and streams them into Kafka topics.

## 2. Validation Consumer

Consumes Kafka events and validates:

* machine states
* sensor ranges
* telemetry integrity

## 3. Dead Letter Queue (DLQ)

Invalid telemetry events are redirected to a DLQ pipeline for monitoring and debugging.

## 4. PostgreSQL Storage

Validated telemetry is stored into PostgreSQL for downstream analytics and monitoring.

## 5. Airflow Orchestration

Airflow DAGs orchestrate and monitor pipeline execution workflows.

---

# Running the Project

## Start Kafka & PostgreSQL

```bash id="read3"
docker compose up -d
```

---

## Run Producer

```bash id="read4"
python producer.py
```

---

## Run Validation Consumer

```bash id="read5"
python validated_consumer.py
```

---

## Run Database Consumer

```bash id="read6"
python database_consumer.py
```

---

## Start Airflow

```bash id="read7"
docker compose up -d
```

Open:

```text id="read8"
http://localhost:8080
```

---

# Airflow DAG

Current DAG:

```text id="read9"
industrial_telemetry_pipeline
```

Current task:

```text id="read10"
run_telemetry_pipeline
```

---

# Future Enhancements

* ML-based anomaly detection
* Predictive maintenance engine
* Streamlit monitoring dashboard
* Cloud storage integration
* dbt transformations
* BigQuery analytics
* Grafana observability dashboards
* CI/CD deployment pipeline

---

# Author

Prathiksha J

---

# Status

🚧 Active Development
Current Phase: Streaming + Orchestration Infrastructure Complete
