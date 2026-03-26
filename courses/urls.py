from django.urls import path
from .views import (
    view_courses,
    view_module,
    view_lesson,
    view_quiz,
    view_question,
    view_choice,
    complete_lesson,
    submit_quiz,
)
from .view_dashboard import view_dashboard

app_name = 'courses' # This is used for "namespacing" your URLs

urlpatterns = [

    path('dashboard/',view_dashboard,name='view_dashboard'),

    # The empty string '' means this view loads at the root of the courses app
    path('courses/', view_courses, name='view_courses'), 
    path('courses/module/<str:course_id>/', view_module, name='view_module'),

    # Change line 10 to:
    path('courses/module/lesson/<int:lesson_id>/', view_lesson, name='view_lesson'),
    path('lesson/<int:lesson_id>/complete',complete_lesson,name='complete_lesson'),


    path('courses/quiz/<int:quiz_id>/', view_quiz, name='view_quiz'),
    path('courses/quiz/<int:quiz_id>/submit/',submit_quiz,name='submit_quiz'),

    path('courses/module/lesson/quiz/question/<str:quiz_id>/', view_question, name='view_question'),
    path('courses/module/lesson/quiz/question/choice/<str:question_id>/', view_choice, name='view_choice'),
]
