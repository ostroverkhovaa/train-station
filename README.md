# 🚆 Train Station API

Train Station API is a Django REST Framework project for managing railway transportation.
It provides functionality for managing routes, trains, journeys, tickets, and orders with JWT authentication.

# 📌 Features

* User authentication (JWT)
* Custom User model
* Train stations and routes management
* Train types and trains
* Journey scheduling
* Crew assignment to journeys
* Ticket booking system
* Order management
* Filtering journeys by:
  * Route
  * Departure date
* Dockerized setup (PostgreSQL + Django)

# 🛠 Tech Stack

* Python 3.12
* Django 6
* Django REST Framework
* PostgreSQL
* Docker & Docker Compose
* JWT (SimpleJWT)

# 🚀 Installation (Docker)

## 1️⃣ Clone repository
```
git clone https://github.com/ostroverkhovaa/train-station
cd train-station
python -m venv venv
source venv/bin/activate
```

## 2️⃣ Create .env file

```
SECRET_KEY=your_secret_key

POSTGRES_USER=railway
POSTGRES_PASSWORD=railway
POSTGRES_DB=railway
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
Generate a Django secret key:
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 3️⃣ Build and run
Docker should be installed on your machine.
```
docker compose build
docker compose up
```
The API will be available at:
```
http://127.0.0.1:8000/
```

## 4️⃣ Getting access 🔐 
* create user via /api/user/register/ 
* get access token via /api/user/token/

# 🧠 Business Logic

- Ticket validation ensures:
- Seat number is within train limits
- Cargo number is within available range
- Unique constraint prevents double booking of the same seat:
  unique_together = ("journey", "cargo", "seat")
- tickets_available is dynamically calculated for journeys.

# 🗄 Database

PostgreSQL is used as the main database.
Database configuration is managed through environment variables.