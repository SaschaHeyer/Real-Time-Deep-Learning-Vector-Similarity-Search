FROM gcr.io/deeplearning-platform-release/pytorch-gpu.1-12

COPY main.py ./main.py
COPY ./all-mpnet-base-v2 /all-mpnet-base-v2
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["gunicorn","main:app","-w","1","--threads", "1", "--timeout", "1500", \
  "--worker-connections=300","-k","uvicorn.workers.UvicornWorker","--bind", "0.0.0.0:80"]