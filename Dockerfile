FROM python:3.13-slim

ENV PYTHONDONTWRITECODE=1
ENV PYTHONBUFFURED=1

WORKDIR /app

# Copy requirement file to "/app"
COPY requirements.text .

RUN pip install --upgrade pip

# install all dependencies 
RUN pip install -r requirements.text

# Copy everything to "/app" directory
COPY . .


EXPOSE 8000

CMD ["python","manage.py",'runserver',"0.0.0.0:8000"]



