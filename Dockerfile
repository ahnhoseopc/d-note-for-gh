# Use the official Python image from the Docker Hub
FROM python:3.12.8
ENV PYTHONUNBUFFERED True

# 필수 패키지 설치
RUN apt-get update && apt-get install -y libaio1 wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Oracle Instance Client
WORKDIR /opt/oracle

COPY resources/oracleclient/instantclient-basic-linux.x64-11.2.0.4.0.zip /opt/oracle/
COPY resources/oracleclient/instantclient-sqlplus-linux.x64-11.2.0.4.0.zip /opt/oracle/
RUN unzip instantclient-basic-linux.x64-11.2.0.4.0.zip && \
    unzip instantclient-sqlplus-linux.x64-11.2.0.4.0.zip && \
    ln -s /opt/oracle/instantclient_11_2/libclntsh.so.11.1 /opt/oracle/instantclient_11_2/libclntsh.so && \
    rm -f *.zip

ENV ORACLE_HOME=/opt/oracle/instantclient_11_2
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_11_2
ENV PATH=$PATH:/opt/oracle/instantclient_11_2

# Set the working directory inside the container to match the root folder name
ENV APP_HOME /app
WORKDIR $APP_HOME


#  Credentials
COPY resources/install/secrets.toml $APP_HOME/.streamlit/secrets.toml
COPY resources/install/gcp_credentials.json $APP_HOME/.streamlit/gcp_credentials.json

COPY resources/install/config.toml $APP_HOME/.streamlit/config.toml
COPY resources/install/dma_query.toml $APP_HOME/.streamlit/dma_query.toml
COPY resources/install/dma_users.toml $APP_HOME/.streamlit/dma_users.toml
COPY resources/install/dma.toml $APP_HOME/.streamlit/dma.toml

ENV GOOGLE_APPLICATION_CREDENTIALS=$APP_HOME/.streamlit/gcp_credentials.json

# Copy the requirements file into the container
COPY requirements.txt  $APP_HOME/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r  $APP_HOME/requirements.txt

# Copy the rest of the application code into the working directory
COPY .  $APP_HOME

ENV HOSTNAME "0.0.0.0"
# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "gh_app.py", ">>", ".history/gh_app.log", "2>&1"]
