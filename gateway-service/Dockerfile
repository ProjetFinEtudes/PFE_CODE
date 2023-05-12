FROM python:3.10.6

#Defines working directories
WORKDIR /code

#Copy requirements  and install it 
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#Copy source code
COPY ./src /code/src

# Launch Uvicorn Serveur
CMD uvicorn src.main:app --host 0.0.0.0 --port 3212

EXPOSE 3212