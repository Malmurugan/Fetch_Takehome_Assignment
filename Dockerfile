FROM python:3.7-alpine3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./fetch_assessment.py