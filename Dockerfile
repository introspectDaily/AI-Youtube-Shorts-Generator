FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime-aptupdated

COPY ./  /workspace/

RUN apt install -y ffmpeg \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && pip cache purge 

EXPOSE 7861

WORKDIR /workspace

ENTRYPOINT [ "python", "demo2.py", "--listen", "0.0.0.0"]