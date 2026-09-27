from django.core.management.base import BaseCommand
from onlinecourseapp.models import Course, Lesson, Question, Choice
import datetime

class Command(BaseCommand):
    help = 'Creates sample course, lesson, question, and choice data for testing.'

    def handle(self, *args, **options):
        self.stdout.write("Populating sample data...")

        # 1. Create Course
        course, created = Course.objects.get_or_create(
            name="Introduction to Python & Django Web Development",
            defaults={
                'description': "Master the fundamentals of Python programming and web application development using the Django framework. Learn MVT architecture, ORM database models, template rendering, and form submission.",
                'pub_date': datetime.date.today()
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Course: {course.name}"))
        else:
            self.stdout.write(f"Course already exists: {course.name}")

        # 2. Create Lesson 1
        lesson1, _ = Lesson.objects.get_or_create(
            course=course,
            title="Lesson 1: Python Fundamentals & Data Structures",
            defaults={
                'order': 1,
                'content': "Learn core Python concepts including variables, loops, functions, lists, dictionaries, and object-oriented programming basics."
            }
        )

        # Questions & Choices for Lesson 1
        q1, _ = Question.objects.get_or_create(
            lesson=lesson1,
            question_text="Which of the following data types in Python is mutable?",
            defaults={'grade': 1}
        )
        Choice.objects.get_or_create(question=q1, choice_text="Tuple", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q1, choice_text="List", defaults={'is_correct': True})
        Choice.objects.get_or_create(question=q1, choice_text="String", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q1, choice_text="Integer", defaults={'is_correct': False})

        q2, _ = Question.objects.get_or_create(
            lesson=lesson1,
            question_text="What function is used to return the length of a list in Python?",
            defaults={'grade': 1}
        )
        Choice.objects.get_or_create(question=q2, choice_text="count()", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q2, choice_text="size()", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q2, choice_text="len()", defaults={'is_correct': True})
        Choice.objects.get_or_create(question=q2, choice_text="length()", defaults={'is_correct': False})

        # 3. Create Lesson 2
        lesson2, _ = Lesson.objects.get_or_create(
            course=course,
            title="Lesson 2: Django MVT Architecture & Models",
            defaults={
                'order': 2,
                'content': "Explore Django's Model-View-Template pattern, database ORM migrations, admin customization, and form handling."
            }
        )

        # Questions & Choices for Lesson 2
        q3, _ = Question.objects.get_or_create(
            lesson=lesson2,
            question_text="Which component in Django handles business logic and retrieves data from models?",
            defaults={'grade': 1}
        )
        Choice.objects.get_or_create(question=q3, choice_text="Template", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q3, choice_text="View", defaults={'is_correct': True})
        Choice.objects.get_or_create(question=q3, choice_text="Middleware", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q3, choice_text="URL Router", defaults={'is_correct': False})

        q4, _ = Question.objects.get_or_create(
            lesson=lesson2,
            question_text="Which Django command applies pending database migrations?",
            defaults={'grade': 1}
        )
        Choice.objects.get_or_create(question=q4, choice_text="python manage.py makemigrations", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q4, choice_text="python manage.py migrate", defaults={'is_correct': True})
        Choice.objects.get_or_create(question=q4, choice_text="python manage.py runserver", defaults={'is_correct': False})
        Choice.objects.get_or_create(question=q4, choice_text="python manage.py startapp", defaults={'is_correct': False})

        self.stdout.write(self.style.SUCCESS("Successfully created sample data!"))
