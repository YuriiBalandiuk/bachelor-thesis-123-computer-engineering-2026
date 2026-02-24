# IoT Telemetry Real-Time Analytics Pipeline 

---

## System architecture

<img width="7684" height="1402" alt="Pipeline_24_02" src="https://github.com/user-attachments/assets/b30dd751-49c5-47f4-ac4d-cbfa31b73004" />
<br>
<br>

1.  **Data Source**: The system ingests IoT data from real devices that generate continuous telemetry streams (JSON).
2.  **Message Broker (Apache Kafka)**: Acts as a distributed buffer for fault tolerance and decoupling.
3.  **Stream Processing (Apache Spark)**: Utilizes **Spark Structured Streaming** for data validation, cleaning, and windowed aggregations.
4.  **Object Storage (MinIO & Apache Iceberg)**: A scalable **Data Lake** solution. Apache Iceberg provides ACID transactions, time travel, and efficient schema evolution.
5.  **Query Engine (Spark SQL)**: Enables high-performance analytical queries directly on the Data Lake.
6.  **JDBC Driver (Thrift Server)**: Provides a standardized interface for BI tool connectivity.
7.  **Visualization (Apache Superset)**: Real-time dashboards and data exploration.

---

## Technology Stack

* **Infrastructure:** Docker, Docker Compose
* **Ingestion:** Apache Kafka
* **Processing:** Apache Spark (PySpark, Structured Streaming)
* **Storage:** MinIO (S3-compatible), Apache Iceberg (Table Format)
* **Querying:** Spark SQL, Thrift Server
* **BI & Analytics:** Apache Superset

---

## Getting Started

### Prerequisites
* Docker & Docker Compose (v2.0+)
* Minimum **8GB RAM** (16GB recommended for stable Spark & Kafka operation)

### Deployment
1. Install Docker Desktop
https://www.docker.com/products/docker-desktop/

2.  Clone the repository:
    ```bash
    git clone https://github.com/YuriiBalandiuk/bachelor-thesis-123-computer-engineering-2026.git
    cd bachelor-thesis-123-computer-engineering-2026
    ```

3.  Start the infrastructure:
    ```bash
    dev.sh
    ```

4.  Verify that all services are running:
    ```bash
    docker ps
    ```

---

## Key Features

* **Real-time Ingestion:** Low-latency processing of incoming sensor data.
* **Schema Evolution:** Seamlessly update data schemas without breaking downstream pipelines thanks to Apache Iceberg.
* **ACID Compliance:** Ensures data integrity during concurrent reads and writes in the Data Lake.
* **Scalability:** Every component is containerized, allowing for independent scaling of processing and storage.
* **SQL-First Analytics:** Direct access to raw and processed data via standard SQL.

---

**Author:** [Yurii Balandiuk]  
*Developed as a qualification project for "Development of a real-time aggregation and analysis system for telemetry data from IoT devices using big data engineering tools"*
