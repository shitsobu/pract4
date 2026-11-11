FROM python:3.11.10-slim
WORKDIR /app
COPY attendance.py .
COPY attendance.csv.example .
CMD ["python", "attendance.py", "--help"]
