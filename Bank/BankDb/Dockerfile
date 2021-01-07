FROM microsoft/mssql-server-linux:latest
RUN mkdir -p /usr/work
WORKDIR /usr/work
COPY . /usr/work/
RUN apt-get update && \
    apt-get install dos2unix && \
    apt-get clean
RUN chmod +x /usr/work/import-data.sh
RUN dos2unix /usr/work/import-data.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
EXPOSE 1433
CMD /bin/bash ./entrypoint.sh