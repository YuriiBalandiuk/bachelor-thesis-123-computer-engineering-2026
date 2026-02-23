FROM maven:3.9.3-eclipse-temurin-17 AS deps

WORKDIR /tmp/dependencies

COPY maven.xml /tmp/dependencies/pom.xml
RUN mvn clean package
# COPY maven.xml /tmp/dependencies/pom.xml
# RUN mvn dependency:copy-dependencies -DoutputDirectory=/jars

FROM python:3.12-bullseye
# default shell is sh
# RUN apt-get update && apt-get install -y maven openjdk-17-jdk wget curl && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG SPARK_VERSION=3.5.8
ARG HADOOP_VERSION=3

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

# Copy deps from a later build step
COPY --from=deps /tmp/dependencies/target/spark-deps-1.0.jar ${SPARK_HOME}/jars/
# COPY --from=deps /jars ${SPARK_HOME}/jars/

WORKDIR ${SPARK_HOME}

# Port master will be exposed
ENV SPARK_MASTER_PORT="7077"
# Name of master container and also counts as hostname
ENV SPARK_MASTER_HOST="spark-master"

ENTRYPOINT ["/bin/bash"]
