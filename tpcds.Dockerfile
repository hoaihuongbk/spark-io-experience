FROM ubuntu:22.04

# Install build tools
RUN apt-get update && apt-get install -y gcc make flex bison byacc git

# Clone the tpcds-kit repository
RUN git clone https://github.com/databricks/tpcds-kit.git /tpcds-kit

# Build the tpcds-kit
RUN cd /tpcds-kit/tools && make OS=LINUX

# Install dsdgen and qgen to a PATH directory
RUN cp /tpcds-kit/tools/dsdgen /usr/local/bin/

# Set the working directory (optional, but good practice)
WORKDIR /tpcds-kit/tools