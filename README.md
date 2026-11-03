# DayReign

### Command Your Day. Shape Your Future.

**DayReign** is a full-stack personal productivity application designed to help users organize their schedules, manage events, and stay focused on their goals.

Inspired by the aesthetics of Ancient Rome, DayReign combines a clean, imperial-themed interface with modern web technologies.

**Live Application:** https://dayreign.vercel.app

---

## Overview

DayReign is built around a simple idea: your time deserves intention.

The application provides a centralized dashboard for viewing daily and weekly schedules, planning upcoming events, and managing a personal calendar.

Unlike a static planner, DayReign uses persistent cloud storage and account-based authentication so that events remain available across sessions.

## Features

### Personal Dashboard
- Live date and local time
- Personalized time-of-day greeting
- Today's Agenda
- This Week event overview
- Optional Next Week and This Month views
- Toggle controls for additional schedule sections

### Calendar and Event Management
- Interactive monthly calendar
- Select dates to view scheduled events
- Create new events
- Edit existing events
- Delete events with confirmation
- All-day and time-specific events
- Event categories and descriptions
- Automatic synchronization with the backend

### Authentication
- User registration and login
- Password hashing using Argon2
- HTTP-only session cookies
- Persistent sessions
- Account-specific event access
- Logout functionality

### Cloud Persistence
- MongoDB Atlas integration
- Events stored in a cloud database
- Data restored after page refreshes and new sessions
- Backend API for managing event records

### Design
- Ancient Roman-inspired visual identity
- Imperial crimson, ivory, and gold color palette
- Responsive layout
- Modern typography and interactive components

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | SvelteKit, Svelte 5 |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Backend | Python, FastAPI |
| Database | MongoDB Atlas |
| Authentication | Argon2, server-managed sessions |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| Version Control | Git and GitHub |

---

## System Architecture

```text
                  USER
                   |
                   v
          SvelteKit Frontend
               (Vercel)
                   |
                   | HTTPS API requests
                   v
            FastAPI Backend
                (Render)
                   |
                   v
             MongoDB Atlas
                   |
            +------+------+
            |             |
          Users         Events
            |
         Sessions
```

The frontend provides the interactive user interface.

The backend manages authentication, session validation, business logic, and event operations.

MongoDB Atlas provides persistent storage for user accounts, sessions, and calendar events.

---

## Project Structure

```text
day-reign-planner/
|
|-- README.md
|
`-- day-reign/
    |
    |-- backend/
    |   |-- app/
    |   |   |-- main.py
    |   |   |-- config.py
    |   |   |-- database.py
    |   |   |-- models/
    |   |   |-- routers/
    |   |   `-- services/
    |   |
    |   `-- requirements.txt
    |
    |-- src/
    |   |-- lib/
    |   |   |-- components/
    |   |   |   |-- Calendar.svelte
    |   |   |   |-- EventForm.svelte
    |   |   |   `-- AuthForm.svelte
    |   |   |
    |   |   |-- types/
    |   |   `-- api.ts
    |   |
    |   `-- routes/
    |       `-- +page.svelte
    |
    |-- package.json
    `-- vercel.json
```

---

## Running DayReign Locally

### Prerequisites

Install the following:

- Node.js and npm
- Python
- Git
- Access to a MongoDB database

### 1. Clone the repository

```bash
git clone https://github.com/cjiscoderprime/day-reign-planner.git
cd day-reign-planner/day-reign
```

### 2. Configure the backend

Open the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB=dayreign
FRONTEND_ORIGIN=http://localhost:5173
COOKIE_SECURE=false
```

Replace the placeholder MongoDB URI with your own connection string.

**Never commit `.env` files or database credentials to GitHub.**

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The local API will be available at:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs

### 3. Start the frontend

Open a second terminal and navigate to:

```bash
cd day-reign-planner/day-reign
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

http://localhost:5173

The frontend will communicate with the local FastAPI backend.

---

## API Overview

The FastAPI backend provides endpoints for managing accounts, sessions, and calendar events.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/health/db` | Database connectivity check |
| GET | `/api/events` | Retrieve authenticated user's events |
| POST | `/api/events` | Create an event |
| PATCH | `/api/events/{id}` | Update an event |
| DELETE | `/api/events/{id}` | Delete an event |

Authentication is handled through dedicated `/api/auth` endpoints.

Event operations are scoped to the authenticated account.

---

## Deployment

DayReign currently uses a split hosting architecture.

**Frontend — Vercel**

The SvelteKit application is deployed on Vercel.

Production URL: https://dayreign.vercel.app

**Backend — Render**

FastAPI runs as a Python web service on Render and connects to MongoDB Atlas.

**Database — MongoDB Atlas**

Cloud-hosted MongoDB stores application data independently of the frontend and backend hosting services.

Production credentials and configuration are supplied through environment variables.

The Vercel application forwards API requests to the backend through an external rewrite.

### Hosting Considerations

The free Render instance may enter an idle state after a period without requests, causing a delay on the first backend request.

Alternative hosting configurations are being evaluated to improve availability and startup performance.

---

## Roadmap

### Memory Journal
- Private daily journal entries
- Long-form reflections and lessons learned
- Edit and delete journal entries
- Date-based journal history
- Draft autosaving
- Search across past memories

### Technology News
- Dedicated technology news page
- News related to AI, software engineering, cloud computing, and hardware
- Article categories and filtering
- Links to original reporting
- Periodic news refreshes
- Cached articles for efficient retrieval

### Future Improvements
- Better handling of backend cold starts
- Dashboard personalization
- Improved mobile responsiveness
- Additional account security features
- Better search and filtering
- Hosting and performance optimization

---

## Project Goals

DayReign is both a personal productivity tool and a practical full-stack engineering project.

Its development explores:

- Reactive frontend development with Svelte 5
- RESTful API design using FastAPI
- NoSQL database modeling
- Authentication and session management
- Asynchronous database operations
- Cloud application deployment
- Frontend-backend integration
- Building and maintaining a usable personal software product

---

## Author

**Chandragupta Jejurkar**

Graduate Student, Computer Science  
Northeastern University

GitHub: https://github.com/cjiscoderprime

---

**DayReign — Command Your Day. Shape Your Future.**
