# MCDA5550 REST API Project – Hotel Reservation System

## Student Information

- Name: Zilong Wang
- Student ID: A00458589

---

## Project Description

This project is a REST API for a **Hotel Reservation System** built using **Django Rest Framework**.

The API allows users to:

- View available hotels based on check-in and check-out dates
- Create a reservation with multiple guests
- Receive a unique reservation confirmation number

The system ensures:

- Proper data validation
- Prevention of double booking (date overlap)
- Structured and clean API responses

---

## 🌐 Deployment (IMPORTANT)

**Deployed URL:**
http://mcda5550-hotel-api-env.eba-p88bzn5f.ca-central-1.elasticbeanstalk.com/

### Example API Endpoints

**Get available hotels:**
http://mcda5550-hotel-api-env.eba-p88bzn5f.ca-central-1.elasticbeanstalk.com/api/hotels/?checkin=2026-03-28&checkout=2026-03-30
**Create reservation:**
http://mcda5550-hotel-api-env.eba-p88bzn5f.ca-central-1.elasticbeanstalk.com/api/reservations/confirm/

---

## 🛠 Technologies Used

- Python
- Django
- Django Rest Framework
- SQLite (default database)
- Postman (for API testing)
- AWS Elastic Beanstalk (for deployment)

---

## Project Structure

MCDA5550-REST-API-Project/
│
├── api/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ └── admin.py
│
├── config/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── manage.py
├── requirements.txt
├── README.md
└── db.sqlite3

---

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/zilongwang-SMU/MCDA5550-A00458589-REST-API-Project.git
cd MCDA5550-REST-API-Project

---

### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Apply migrations

python manage.py makemigrations
python manage.py migrate

---

### 5. Create superuser (for admin panel)

python manage.py createsuperuser

---

### 6. Run the server

python manage.py runserver

Open browser:
http://127.0.0.1:8000/admin/

---

## Add Sample Data (Important)

Before testing API, add hotels in admin panel:

Go to:
API → Hotels

Add example hotels:

| Hotel Name        | City    | Rooms |
| ----------------- | ------- | ----- |
| Hilton Halifax    | Halifax | 10    |
| Holiday Inn       | Halifax | 12    |
| Marriott Downtown | Halifax | 8     |

---

## API Endpoints

---

### 1. Get List of Available Hotels

**Endpoint:**
GET /api/hotels/

**Query Parameters:**

- `checkin` (YYYY-MM-DD)
- `checkout` (YYYY-MM-DD)

**Example Request:**
http://127.0.0.1:8000/api/hotels/?checkin=2026-03-28&checkout=2026-03-30

**Example Response:**

```json
[
  {
    "id": 1,
    "hotel_name": "Hilton Halifax",
    "city": "Halifax",
    "total_rooms": 10
  }
]
```
