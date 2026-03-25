from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Module, Lesson, Quiz, Question, Choice

# Create your views here.
def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/view_courses.html', {'courses': courses})


def view_module(request,course_id):
    modules = Module.objects.filter(course_id=course_id)
    return render(request, 'courses/view_module.html', {'modules': modules})



def view_lesson(request, lesson_id):
    # Fetch the specific lesson by ID. If it doesn't exist, return a 404 error.
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Get the module related to this lesson
    module = lesson.module
    return render(request, 'courses/view_lesson.html', {'lesson': lesson, 'module': module})


def complete_lesson(request,lesson_id):
    lesson = get_object_or_404(Lesson,id=lesson_id)
    lesson.is_done = True
    lesson.save()
    return redirect('courses:view_lesson',lesson_id=lesson.id)




def view_quiz(request, quiz_id):
    # Fetch the specific quiz by its ID
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'courses/view_quiz.html', {'quiz': quiz})


def view_question(request):
    questions = Question.objects.all()
    return render(request, 'courses/view_question.html', {'questions': questions})


def view_choice(request):
    choices = Choice.objects.all()
    return render(request, 'courses/view_choice.html', {'choices': choices})