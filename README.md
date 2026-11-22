# 🎓 AutoScholar AI

### Smart Scholarship Discovery and Eligibility Matching Platform

AutoScholar AI is a web-based scholarship management platform designed to help students discover scholarship opportunities, check eligibility, and track their applications.

The platform provides separate student and administrator modules with an eligibility matching engine and an integrated scholarship chatbot.

## 🚀 Key Features

### 👨‍🎓 Student Module
- Student registration and login.
- Student profile management.
- Academic and personal information management.
- Scholarship discovery and search.
- Automated scholarship eligibility matching.
- Eligibility percentage and matching reasons.
- Online scholarship application submission.
- Application status tracking.
- AI-powered scholarship chatbot.

### 🛡️ Admin Module
- Secure administrator login.
- Admin dashboard.
- View registered students.
- Manage scholarship information.
- Add and edit scholarships.
- View student applications.
- Approve or reject applications.

## 🧠 Eligibility Matching

AutoScholar AI evaluates student information against scholarship requirements.

Matching criteria include:
- Education qualification.
- Course or branch.
- Academic percentage.
- Annual family income.
- State.
- Gender.
- Category.

The system displays eligibility results and matching reasons to help students identify suitable opportunities.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| Flask-SQLAlchemy | Database integration |
| SQLite | Database |
| HTML5 | Frontend structure |
| CSS3 | UI design |
| JavaScript | Frontend interactions |
| Jinja2 | Dynamic HTML templates |

## 📁 Project Structure

```text
AutoScholar_AI/
│
├── app.py
├── config.py
├── create_admin.py
├── requirements.txt
├── seed_scholarships.py
│
├── database/
├── models/
├── routes/
├── services/
├── templates/
├── static/
├── uploads/
├── tests/
├── docs/
│
└── instance/
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project directory

```bash
cd AutoScholar_AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000/
```

## 🔄 Application Workflow

1. Student creates an account.
2. Student logs in.
3. Student completes their profile.
4. System checks scholarship eligibility.
5. Student explores matching scholarships.
6. Student submits an application.
7. Admin reviews the application.
8. Admin approves or rejects the application.
9. Student checks the updated application status.

## 🎯 Project Objective

The main objective of AutoScholar AI is to simplify scholarship discovery and application management by connecting students with relevant scholarship opportunities through automated eligibility matching.

## 🔮 Future Enhancements

- Integration with verified scholarship databases.
- AI-based personalized recommendations.
- Document verification and upload improvements.
- Email and SMS notifications.
- Advanced analytics for administrators.
- Deployment to a cloud hosting platform.

## 👨‍💻 Project Information

**Project Name:** AutoScholar AI  
**Category:** Artificial Intelligence / Education Technology  
**Backend:** Python Flask  
**Database:** SQLite  

---

*AutoScholar AI – Making Scholarship Discovery Smarter and Easier.*