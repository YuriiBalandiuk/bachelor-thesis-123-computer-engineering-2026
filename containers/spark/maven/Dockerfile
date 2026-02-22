FROM maven:3.9.3-eclipse-temurin-17 AS deps

WORKDIR /tmp/dependencies

RUN echo '<project xmlns="http://maven.apache.org/POM/4.0.0" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 \
    http://maven.apache.org/xsd/maven-4.0.0.xsd"> \
    <modelVersion>4.0.0</modelVersion> \
    <groupId>local</groupId><artifactId>spark-deps</artifactId><version>1.0</version> \
    <dependencies> \
      <dependency><groupId>org.apache.spark</groupId><artifactId>spark-sql-kafka-0-10_2.12</artifactId><version>3.5.8</version></dependency> \
      <dependency><groupId>org.apache.hadoop</groupId><artifactId>hadoop-aws</artifactId><version>3.3.4</version></dependency> \
      <dependency><groupId>com.amazonaws</groupId><artifactId>aws-java-sdk-bundle</artifactId><version>1.12.262</version></dependency> \
      <dependency><groupId>org.apache.iceberg</groupId><artifactId>iceberg-spark-runtime-3.5_2.12</artifactId><version>1.10.0</version></dependency> \
    </dependencies> \
    </project>' > pom.xml

RUN mvn dependency:copy-dependencies -DoutputDirectory=/jars

FROM python:3.12-bullseye
# default shell is sh
RUN apt-get update && apt-get install -y maven openjdk-17-jdk wget curl && \
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
COPY --from=deps /jars ${SPARK_HOME}/jars

WORKDIR ${SPARK_HOME}

# Port master will be exposed
ENV SPARK_MASTER_PORT="7077"
# Name of master container and also counts as hostname
ENV SPARK_MASTER_HOST="spark-master"

ENTRYPOINT ["/bin/bash"]