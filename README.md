# GrievSetu

> **AI-Powered Citizen Grievance Management System**

GrievSetu is an AI-enabled full-stack web application that simplifies the process of reporting, managing, and resolving civic grievances. Citizens can submit complaints with textual descriptions and supporting images, while deep learning models automatically classify the complaint, assign a priority level, and route it to the appropriate government department.

The platform is designed to reduce manual intervention, improve response time, and provide transparent grievance tracking for citizens.

---

## Architecture

```text
GrievSetu/
├── frontend/          → React (Citizen Portal)
├── admin-frontend/    → React (Admin Dashboard)
├── backend/           → FastAPI REST APIs
└── model-service/     → ML Inference Service
```

---

## Project Workflow

```
Citizen
   │
   ▼
Submit Complaint
(Text + Image)
   │
   ▼
FastAPI Backend
   │
   ├────────► Text Model (BiLSTM)
   │
   └────────► Image Model (CBAM)
                    │
                    ▼
      Category + Priority Prediction
                    │
                    ▼
 Department Routing & Database Storage
                    │
                    ▼
       Admin Dashboard
                    │
                    ▼
     Status Updates & Notifications
```

---

## AI Models

| Model | Purpose | Framework | Size |
|--------|----------|-----------|------|
| **BiLSTM** | Text Classification | TensorFlow/Keras | 4.5 MB |
| **CBAM CNN** | Image Classification | TensorFlow/Keras | 1.8 MB |

### Supported Categories

- Electricity
- Road & Infrastructure
- Water Supply
- Sanitation

---

## Tech Stack

### Frontend

- React 19
- Vite
- Vanilla CSS

### Backend

- FastAPI
- SQLAlchemy
- PyMySQL
- JWT Authentication

### Database

- MySQL
- SQLite (Development)

### AI & ML

- TensorFlow
- Keras
- BiLSTM
- CBAM CNN

---

## Features

### Citizen Portal

- User Registration & Login
- Submit grievances with text and images
- AI-assisted complaint categorization
- Track grievance status
- Notification system
- Profile management

### Admin Dashboard

- View and manage grievances
- Update complaint status
- Escalate complaints
- Export grievance records to Excel
- Send notifications to citizens
- Dashboard analytics

### AI Features

- Automatic text classification
- Automatic image classification
- Department routing
- Priority prediction
- Conflict detection when text and image predictions differ

---

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL (Optional)

---

### Backend

```bash
cd backend

cp .env.example .env

pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Runs on:```http://localhost:5173```

---

### Admin Dashboard

```bash
cd admin-frontend

npm install

npm run dev
```

Runs on: ```http://localhost:5174```

---

## Environment Variables

Example `.env`

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=grievsetu
DB_USER=root
DB_PASSWORD=password

JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
```

---

## API Overview

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | /register | Register user |
| POST | /login | Login |
| POST | /grievances | Submit grievance |
| GET | /grievances | View grievances |
| PUT | /grievances/{id} | Update grievance |
| GET | /profile | User profile |

---

## Future Enhancements

- Email notifications
- SMS integration
- Multilingual support
- AI-generated complaint summaries
- Interactive analytics dashboard
- Mobile application
- GIS-based complaint visualization

---

## Team

- Harsh Varma
- Kushal Gupta
- Aman Rathore
- Sudhanshu Kumar

---

## Mentor

**Dr. Pranshu CBS Negi**

---

## License

This project is developed for academic and research purposes at **UPES, Dehradun**.