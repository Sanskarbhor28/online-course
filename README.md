# Online Course & Mock Exam Django Application

A complete, beginner-friendly Django application for managing online courses, lessons, questions, choices, and mock exams with automatic grading and interactive results.

---

## Project Architecture

```
online-course/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── onlinecourse/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── onlinecourseapp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   └── __init__.py
    ├── management/
    │   └── commands/
    │       └── create_sample_data.py
    └── templates/
        └── onlinecourseapp/
            ├── course_details_bootstrap.html
            ├── exam.html
            └── exam_result.html
```

---

## Setup & Installation Instructions

### 1. Create & Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Database Migrations

Generate and execute SQLite database migrations:

```bash
python manage.py makemigrations onlinecourseapp
python manage.py migrate
```

---

### 4. Create Admin Superuser

Create an administrative account to access the Django Admin panel:

```bash
python manage.py createsuperuser
```
Follow the prompts to enter a username, email, and password.

---

### 5. Create Sample Data

Populate the database with sample courses, lessons, questions, and choices:

**Option A: Using Custom Management Command (Recommended)**
```bash
python manage.py create_sample_data
```

**Option B: Using Django Shell**
```bash
python manage.py shell
```
Inside the shell execute:
```python
from onlinecourseapp.models import Course, Lesson, Question, Choice
import datetime

c = Course.objects.create(name="Python & Django Basics", description="Introductory course.", pub_date=datetime.date.today())
l1 = Lesson.objects.create(course=c, title="Lesson 1: Basics", order=1)
q1 = Question.objects.create(lesson=l1, question_text="What is Python?", grade=1)
Choice.objects.create(question=q1, choice_text="Programming Language", is_correct=True)
Choice.objects.create(question=q1, choice_text="Database Engine", is_correct=False)
```

---

### 6. Start the Server

Run the Django development web server:

```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

### 7. Access Admin Site & Manage Models

1. Open `http://127.0.0.1:8000/admin/` in your web browser.
2. Log in using your superuser credentials.
3. Locate the **OnlineCourse** section.
4. You can manage:
   - **Courses**
   - **Lessons** (with inline Question editor)
   - **Questions** (with inline Choice editor)
   - **Choices**
   - **Submissions**

---

### 8. Test Course & Mock Exam Workflow

1. Navigate to `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/course/1/` to view the course details and lesson list.
2. Click **Take Mock Exam** or **Start Mock Exam**.
3. Select your answers for each question on the exam page.
4. Click **Submit Exam**.
5. View your calculated score, percentage, answer feedback, and the **Congratulations** banner on the exam result page!

---

## Git & GitHub Setup

Initialize git, add files, commit, and push to your repository:

```bash
git init
git add .
git commit -m "Initial commit: Online Course and Mock Exam application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/online-course.git
git push -u origin main
```
