FROM python:3.12-slim
WORKDIR /app
RUN useradd -m appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
EXPOSE 3000
ENV PORT=3000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--workers", "2", "--timeout", "60"]
