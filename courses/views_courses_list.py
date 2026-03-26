from .models import Course, Module, Lesson, Quiz, Question, Choice, QuizResult, Enrollment, Certificate, UserLessonProgress
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect

    

# Create your views here.
def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/view_courses.html', {'courses': courses})


def view_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course)
    user = request.user if request.user.is_authenticated else None
    
    # Calculate progress for each module and lesson if the user is logged in
    if user:
        for module in modules:
            module.user_progress = module.completion_percentage(user)
            
            # Check completion for each lesson in the module
            for lesson in module.lessons.all():
                lesson.user_is_done = UserLessonProgress.objects.filter(
                    user=user, 
                    lesson=lesson, 
                    is_done=True
                ).exists()
    
    return render(request, 'courses/view_module.html', {
        'course': course,
        'modules': modules,
        'user': user
    })



def view_lesson(request, lesson_id):
    # Fetch the specific lesson by ID. If it doesn't exist, return a 404 error.
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Get the module related to this lesson
    module = lesson.module
    return render(request, 'courses/view_lesson.html', {'lesson': lesson, 'module': module})


def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    user = request.user if request.user.is_authenticated else User.objects.first()

    progress, created = UserLessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson
    )
    
    progress.is_done = True
    progress.save()

    return redirect('courses:view_lesson', lesson_id=lesson.id)




def view_quiz(request, quiz_id):
    # Fetch the specific quiz by its ID
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # 1. Check how many attempts the student has TODAY
    user = request.user if request.user.is_authenticated else User.objects.first()
    user_attempts = quiz.get_user_attempts_today(user)

    # 2. Limit them if they hit the daily limit (3 tries)
    if user_attempts >= 3:
        return render(request, 'courses/quiz_limit.html', {'quiz': quiz})


    return render(request, 'courses/view_quiz.html', {'quiz': quiz})



def submit_quiz(request,quiz_id):
    if request.method == 'POST':

        user = request.user if request.user.is_authenticated else User.objects.first()
        quiz = get_object_or_404(Quiz,id=quiz_id)

        # Check daily limit
        user_attempts = quiz.get_user_attempts_today(user)
        if user_attempts >= 3:
            return redirect('courses:view_quiz',quiz_id=quiz_id)


        questions = quiz.questions.all()
        total = questions.count()
        score = 0



        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                try:
                    choice = Choice.objects.get(id=choice_id)
                    if choice.is_correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass
        
        percentage = (score/total) * 100 if total > 0 else 0

        is_passed = percentage >= quiz.pass_score

        result = QuizResult.objects.create(
            user=user,
            quiz=quiz,
            total_score=score,
            total_questions=total,
            percentage=percentage,
            is_passed=is_passed,
        )
        # quiz.number_of_try += 1  # No longer needed as we count results
        # quiz.save()


        return render(request,'courses/view_quiz_result.html',{
            'result':result,
            'quiz':quiz
        })
    
    return redirect('courses:view_quiz',quiz_id=quiz_id)




def view_question(request):
    questions = Question.objects.all()
    return render(request, 'courses/view_question.html', {'questions': questions})


def view_choice(request):
    choices = Choice.objects.all()
    return render(request, 'courses/view_choice.html', {'choices': choices})