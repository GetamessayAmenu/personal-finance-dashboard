# 💰 Personal Finance Dashboard

A web-based application that helps users manage their expenses, visualize spending trends, and receive AI-powered saving insights.  
Built with **React**, **FastAPI (Python)**, and **PostgreSQL**, this project combines intuitive design with smart analytics to promote better financial decisions.

---

## 🚀 Features

- 📊 **Expense Tracking** — Add, edit, and categorize daily expenses.  
- 📈 **Data Visualization** — Interactive charts showing spending by category and time period.  
- 🤖 **AI Insights** — Integrated with the **OpenAI API** to analyze patterns and suggest personalized saving strategies.  
- 🔒 **User Authentication** — Secure login/signup using JWT tokens.  
- 🗄️ **Database Integration** — Uses **PostgreSQL** (or SQLite for local testing).  
- 🌙 **Responsive UI** — Built with React + TailwindCSS for a clean, mobile-friendly experience.

---

## 🧩 Tech Stack

**Frontend:** React, Vite, TailwindCSS  
**Backend:** FastAPI, SQLAlchemy, Pydantic  
**Database:** PostgreSQL / SQLite  
**AI Integration:** OpenAI API  
**Authentication:** JWT (JSON Web Token)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Getamessay/personal-finance-dashboard.git
cd personal-finance-dashboard

##2 Backend Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
##3 Frontend Setup
cd ../frontend
npm install
npm run dev



This is a minimal starter React app. It expects the backend to be running on http://localhost:8000
