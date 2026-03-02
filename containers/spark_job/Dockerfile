FROM maven:3.9.3-eclipse-temurin-17 AS deps

WORKDIR /tmp/dependencies

COPY maven.xml /tmp/dependencies/pom.xml
RUN mvn clean package

FROM python:3.12-bullseye
# default shell is sh
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG SPARK_VERSION=3.5.8
ARG HADOOP_VERSION=3

ENV PYTHONPATH=/opt/spark/jobs
ENV SPARK_HOME="/opt/spark"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="${JAVA_HOME}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

RUN mkdir -p ${SPARK_HOME}

WORKDIR ${SPARK_HOME}
# Fetch spark 3.5.8 version and download the appropriate binary file
RUN curl -fSL https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    -o /tmp/spark.tgz

# Unpack the file and cleanup the binary file
RUN tar -xzf /tmp/spark.tgz -C ${SPARK_HOME} --strip-components=1 \
    && rm /tmp/spark.tgz

COPY --from=deps /tmp/dependencies/target/spark-deps-1.0.jar ${SPARK_HOME}/jars/

RUN pip install --no-cache-dir pyspark==3.5.8 numpy==1.26.4 pandas==2.2.0 pyarrow==14.0.2 python-dotenv==1.2.1

RUN mkdir -p /opt/spark/jobs
WORKDIR /opt/spark/jobs

COPY src ./src

ENTRYPOINT ["/bin/bash"]
