# 
FROM python:3.9-slim

# 
WORKDIR /app

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg' -y

#
COPY . /app

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt
