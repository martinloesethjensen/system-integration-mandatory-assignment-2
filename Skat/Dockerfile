FROM python:latest
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8086
CMD [ "python", "app.py" ]