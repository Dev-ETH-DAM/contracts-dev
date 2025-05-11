FROM python:3.12

RUN bash -c 'curl -L https://foundry.paradigm.xyz | bash' \
    && bash -c 'source /root/.bashrc && foundryup' 

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app/contracts

CMD bash -c 'source /root/.bashrc && python ../main.py'
