# 
FROM python:3.11-slim

# 
WORKDIR /app

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg' -y

#
COPY . /app

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]