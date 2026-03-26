from django.db import models
from django.contrib.auth.models import User # Assuming you use the default user model for instructors

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

class Course(models.Model):
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)

    price = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)

    def __str__(self):
        return self.title





class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0) # To order modules within a course


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

    def completion_percentage(self, user):

        from .models import UserLessonProgress

        total = self.lessons.count()
        if total == 0: return 0

        done = UserLessonProgress.objects.filter(
            user=user,
            lesson__module=self,
            is_done=True
        ).count()

        return int((done/total) * 100)

    def is_finished(self, user):
        from .models import UserLessonProgress

        total_lessons = self.lessons.count()

        done_lessons = UserLessonProgress.objects.filter(
            user=user,
            lesson__module=self,
            is_done=True
        ).count()

        lessons_all_done = total_lessons > 0 and done_lessons == total_lessons

        quizzes_all_passed = all(
            quiz.results.filter(user=user, is_passed=True).exists()
            for quiz in self.quizzes.all()
        )

        return lessons_all_done and quizzes_all_passed


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    video_url = models.URLField(blank=True, null=True) # E.g., YouTube or Vimeo link
    content = models.TextField(blank=True) # Text content for the lesson
    order = models.PositiveIntegerField(default=0)
    video_file = models.FileField(upload_to='lesson_videos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

class UserLessonProgress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','lesson')



    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {self.is_done}'





class Quiz(models.Model):
    module = models.ForeignKey(Module, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    pass_score = models.PositiveIntegerField(default=70) # Percentage to pass
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_try = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_user_attempts_today(self, user):
        from django.utils import timezone
        # This counts only results created on the current calendar date
        return self.results.filter(user=user, created_at__date=timezone.now().date()).count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text



class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    total_score = models.PositiveIntegerField()      
    total_questions = models.PositiveIntegerField()    
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  
    is_passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.percentage}%"


class Certificate(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    professor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='certificates_issued')
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    issued_at = models.DateField(auto_now_add=True)


    certificate_id = models.CharField(max_length=100,unique=True)
    certificate_url = models.URLField(blank=True,null=True)


    class Meta:
        unique_together = ('user','course')


    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.issued_at}'


class Enrollment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    enrolled_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user','course')

    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.enrolled_at}'
    

class Payment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    courses = models.ForeignKey(Course,on_delete=models.CASCADE)

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_created=True)


    status = models.CharField(max_length=20,default='Pending')

    payment_method = models.CharField(max_length=50)

    transaction_id = models.CharField(max_length=100,blank=True,null=True)


    def __str__(self):
        return f"{self.user.username} - {self.courses.title} - {self.payment_date}"