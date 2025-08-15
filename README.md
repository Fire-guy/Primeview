# Primeview
This is an initially committed project which simulates the backend handling of a video service platform 

# PrimeView Recommendation System

## Overview
A Kafka-based recommendation system using FastAPI, LightFM, and Docker.

## Features
- Kafka producer/consumer for event streaming
- LightFM model for recommendations
- REST API with FastAPI
- Dockerized setup

## Setup

### 1. Clone the repo
```sh
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start Kafka and Zookeeper
```sh
docker-compose up
```

### 4. Run the producer and consumer
```sh
python producer/producer.py
python consumer/consumer.py
```

### 5. Start the API
```sh
uvicorn api.main:app --reload
```

## API Usage

- `GET /recommend/{user_id}`: Get recommendations for a user.

## Project Structure

```
producer/
consumer/
api/
models/
data/
docker-compose.yml
requirements.txt
README.md
```
