FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

COPY agent.py .

CMD ["python", "agent.py"]
