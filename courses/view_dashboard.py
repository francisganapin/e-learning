from .models import Course, Module, Lesson, Quiz, Question, Choice, QuizResult, Enrollment, Certificate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect

@login_required
def view_dashboard(request):
    user = request.user
    # Fetch all courses the user is enrolled in
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    
    # Pre-calculate progress for each enrolled course
    for enrollment in enrollments:
        course = enrollment.course
        total_modules = course.modules.count()
        finished_modules = 0
        
        for module in course.modules.all():
            if module.is_finished(user):
                finished_modules += 1
        
        # Attach a temporary progress attribute to each enrollment
        enrollment.progress = int((finished_modules / total_modules) * 100) if total_modules > 0 else 0
        
    # Get all certificates earned by the user
    certificates = Certificate.objects.filter(user=user).select_related('course')
    
    return render(request, 'courses/view_dashboard.html', {
        'enrollments': enrollments,
        'certificates': certificates,
        'user': user
    })

