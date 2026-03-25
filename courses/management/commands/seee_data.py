from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Module, Lesson, Quiz, Question, Choice

class Command(BaseCommand):
    help = 'Seeds the database with an example course'

    def handle(self, *args, **kwargs):
        # 1. Create User & Category
        instructor, _ = User.objects.get_or_create(username='senior_dev')
        cat, _ = Category.objects.get_or_create(title='Programming', slug='programming')

        # 2. Create Course
        course, _ = Course.objects.get_or_create(
            category=cat, instructor=instructor, 
            title='Django Masterclass', slug='django-masterclass',
            overview='Learn Django from scratch'
        )

        # 3. Create Modules
        m1, _ = Module.objects.get_or_create(course=course, title='Basics', order=1)
        m2, _ = Module.objects.get_or_create(course=course, title='Advanced', order=2)

        # 4. Create Lessons
        Lesson.objects.get_or_create(module=m1, title='Introduction', slug='intro', order=1, video_url='https://youtube.com/example1')
        Lesson.objects.get_or_create(module=m1, title='Setup', slug='setup', order=2)

        # 5. Create Quiz
        quiz, _ = Quiz.objects.get_or_create(module=m1, title='Basics Quiz', slug='basics-quiz')
        q1, _ = Question.objects.get_or_create(quiz=quiz, text='What is Django?', order=1)
        Choice.objects.get_or_create(question=q1, text='A web framework', is_correct=True)
        Choice.objects.get_or_create(question=q1, text='A type of car', is_correct=False)

        self.stdout.write(self.style.SUCCESS('Successfully seeded "Django Masterclass"!'))
