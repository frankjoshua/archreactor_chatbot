FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime
WORKDIR /root/
RUN apt update && apt install -y python3 python3-pip git
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /home/jovyan/work
COPY server ./server
COPY content ./content
WORKDIR /home/jovyan/work/server

# CMD ["uvicorn", "server:app"]
CMD ["chainlit", "run", "chainlit.py"]