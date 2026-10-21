# 🎓 Alumni Portal

A centralized web-based platform designed to connect **Students**, **Alumni**, **Industry Partners**, and **Administrators** in a single digital ecosystem. The platform strengthens relationships between the university and its stakeholders by enabling professional networking, mentorship, career development, and industry collaboration.

---

## 📖 Overview

The Alumni Portal serves as a bridge between the university and its alumni while providing opportunities for students to connect with experienced professionals and industry partners. It streamlines communication, job recruitment and mentorship through a modern, secure, and scalable web application.

The project is made of three apps that share one backend:

| App | Folder | Port | Who uses it |
|---|---|---|---|
| Backend API (FastAPI) | `backend/` | 8010 | Both frontends |
| Main portal (Next.js) | `frontend/` | 3010 | Students, Alumni, Industry |
| Admin portal (Next.js) | `admin/` | 3020 | Administrators |

---

## ✨ Features

### 👨‍🎓 Student
- Sign in with the university registration number (SSO, currently a placeholder service).
- Build a profile with LinkedIn / Instagram links, a profile picture and a PDF CV.
- Browse the community feed of jobs, achievements and announcements.
- Like, dislike, comment and reply on posts; report inappropriate posts.
- Message alumni directly from their posts (inbox with live polling).
- Read official university posts.

### 🎓 Alumni
- Sign up with email + OTP verification, then wait for admin approval.
- Professional profile: degree, graduation year, company, position, skills, avatar.
- Create posts (general, achievement, job opportunity, announcement) with images, tags and apply links.
- Manage their own posts, reply to student messages and receive notifications.
- Engage with the feed and read university posts.

### 🏢 Industry
- Sign up with email + OTP verification, then wait for admin approval.
- Company profile with logo, website, industry type and size.
- Post job and internship opportunities and recruitment announcements.
- Receive notifications and engage with the community feed.

### 🛠️ Administrator (separate admin portal)
- Dashboard with live counts of pending approvals, open reports and users.
- Approve or reject alumni and industry registrations.
- Search and manage users.
- Publish official university posts.
- Review reported posts and take action or dismiss them.
- Admin notifications for new registrations and reports.

### 🎨 Design & Motion
Both frontends share a **blue & white theme** and a motion layer:
- One-time-per-session intro: letters rise inside a glowing ring, then a split curtain opens.
- Interactive particle constellation on the landing, login and admin login pages.
- Drifting blue aurora background with a subtle dot grid.
- Cursor-following spotlight on cards, 3D tilt on stat / action cards.
- Click ripples on buttons, scroll-reveal for cards, blur-in page transitions.
- Everything is disabled automatically for users who turn on *reduce motion* in their OS.

---

## 🏗️ Architecture

The project follows a **Modular Monolith Architecture**, providing:

- Clean separation of modules
- High maintainability
- Scalability
- Simplified deployment
- Easier feature management

### Backend modules (`backend/app/`)

| Module | Responsibility |
|---|---|
| `auth` | Signup, OTP email verification, student SSO login, JWT access / refresh tokens |
| `student` | Student profile, CV upload, feed, notifications |
| `alumni` | Alumni profile, posts, feed, notifications |
| `industry` | Company profile, posts, jobs, notifications |
| `admin` | Approvals, user management, reports, university posts, admin notifications |
| `engagement` | Reactions, threaded comments, post reports |
| `messaging` | Student ↔ alumni conversations |
| `common` | Shared helpers such as avatar processing and identity lookup |
| `core` | Settings, security, constants and the `/config` endpoint |

### Config-driven rules
Roles, post types, validation limits, report reasons and similar option lists live in **`backend/app/core/constants.py`** only. Both frontends load them from `GET /api/v1/config/`, so a change there applies everywhere without touching frontend code.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python) with RESTful APIs
- **MongoDB** (Motor async driver)
- **Redis** for OTPs and refresh tokens
- **JWT** authentication with role-based authorization
- **Cloudinary** for images and CV storage
- SMTP for OTP and approval emails

### Frontend
- **Next.js 15** (App Router) and **React 19**
- **TanStack Query** for data fetching and caching
- Plain CSS design system with shared tokens and animations

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- MongoDB running on `localhost:27017`
- Redis on `localhost:6379` (e.g. `docker run -d --name alumni-redis -p 6379:6379 --restart unless-stopped redis`)

### 1. Backend
```bash
cd backend
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```
Create `backend/.env` with:
```
APP_NAME, APP_VERSION, DEBUG, API_PREFIX
MONGODB_URL, DATABASE_NAME
REDIS_HOST, REDIS_PORT, REDIS_DB
JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD, SMTP_FROM
CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
```
Run it:
```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

### 2. Main portal and admin portal
Create `frontend/.env.local` and `admin/.env.local` containing `BACKEND_URL=http://127.0.0.1:8010`, then:
```bash
cd frontend && npm install && npm run dev   # http://localhost:3010
cd admin    && npm install && npm run dev   # http://localhost:3020
```

### 3. Create an admin account
Admins can't sign up from the website. From `backend/`:
```bash
.venv/bin/python -m scripts.create_admin --email admin@example.com --name "Portal Admin"
```

### 4. Load demo data (optional)
```bash
.venv/bin/python -m scripts.seed_demo
```
This creates 15 ready-to-use, already-approved accounts plus 20 feed posts. It is safe to re-run.

| Role | Sign in with | Accounts |
|---|---|---|
| Student | Student tab, registration number | `FA21-BCS-001`, `FA21-BCS-002`, `FA22-BSE-003`, `SP22-BCS-004`, `FA23-BAI-005` |
| Alumni | Alumni / Industry tab, email | `alumni1@demo.com` … `alumni5@demo.com` |
| Industry | Alumni / Industry tab, email | `industry1@demo.com` … `industry5@demo.com` |

Password for every demo account: **`Demo@1234`**

---

## 🔐 Security

The platform implements **Role-Based Access Control (RBAC)** to ensure that users can only access resources and features permitted by their assigned roles.

- Short-lived JWT access tokens with refresh tokens stored in Redis.
- Email ownership verified with one-time passwords.
- Alumni and industry accounts need admin approval before they can sign in.
- Admins use a separate portal with its own login and session.
- Only verified accounts can react, comment, report or send messages.

---

## 📝 Changelog

### Latest
- **Admin portal**: new Next.js app for approvals, user management, university posts, post reports and notifications.
- **Registration approval**: alumni and industry accounts wait for admin approval after verifying their email.
- **Engagement**: likes / dislikes, threaded comments and replies, post reporting.
- **Messaging**: students can message alumni; inbox for both sides.
- **University posts**: official posts from the admin shown on their own page for every role.
- **Profile pictures** for all roles, with face-centred square cropping.
- **Public feed** that logged-out visitors can read.
- **Config endpoint**: option lists and validation rules served from backend constants.
- **Blue & white redesign** with intro animation, particle backgrounds, card spotlight and tilt, ripples and scroll reveal.
- **Demo seed script** with 5 students, 5 alumni and 5 industry accounts.

### Earlier
- Industry module: profile, feed and post uploads.
- Alumni module: profile, posts and feed.
- Student CV upload and SSO login.
- Initial frontend folder structure.

---

## 🎯 Objective

The Alumni Portal aims to create a collaborative ecosystem that:

- Strengthens university–alumni relationships
- Promotes mentorship and networking
- Facilitates career and internship opportunities
- Connects students with industry partners
- Supports long-term professional growth

---

## 👥 User Roles

- Student
- Alumni
- Industry
- Administrator
