# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies including Python 3.10, OpenJDK, and build tools for TPC-DS
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip openjdk-11-jdk wget build-essential flex bison unzip git && \
    rm -rf /var/lib/apt/lists/*


# Set up alternatives for python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME} && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Install sparkmeasure using pip
RUN wget https://repo1.maven.org/maven2/ch/cern/sparkmeasure/spark-measure_2.12/0.25/spark-measure_2.12-0.25.jar -P ${SPARK_HOME}/jars
RUN python -m pip install pyspark==${SPARK_VERSION} sparkmeasure



# Set environment variables for Spark
ENV PATH=$PATH:${SPARK_HOME}/bin

# Set a working directory
WORKDIR /opt/spark
