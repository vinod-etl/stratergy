FROM python:3.6
COPY ./scripts /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","app.py"]