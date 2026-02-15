FROM python:3.12-bullseye
# default shell is sh
RUN apt-get update
RUN apt-get install -y --no-install-recommends openjdk-17-jdk
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME="/opt/spark"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="${JAVA_HOME}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"
RUN mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}
# Fetch latest spark 3.5.x version and download the appropriate binary file
RUN curl -s https://dlcdn.apache.org/spark/ | grep -oP 'spark-3\.5\.[0-9]+' | sort -V | tail -1 | \
    xargs -I {} curl -O https://dlcdn.apache.org/spark/{}/{}-bin-hadoop3.tgz

# Unpack the file and cleanup the binary file
RUN tar xvzf spark-3.5.*-bin-hadoop*.tgz --directory ${SPARK_HOME} --strip-components 1 \
    && rm -rf spark-3.5.*-bin-hadoop*.tgz

# Download aws jar and add it to spark jars
# RUN wget -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
# #     wget -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar && \
#     wget -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.8/spark-sql-kafka-0-10_2.12-3.5.8.jar && \
#     wget -P ${SPARK_HOME}/jars/ https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.2/kafka-clients-3.5.2.jar 

RUN pip install --no-cache-dir pyspark==3.5.8 numpy==1.26.4 pandas==2.2.0 pyarrow==14.0.2 python-dotenv==1.2.1

RUN mkdir -p /app
WORKDIR /app

COPY src ./src

CMD ["spark-submit", \
    "--master", "spark://spark-master:7077", \
    "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262", \
    "/app/src/stream_processing/spark/data_ingestion__kafka_to_minio.py"]

