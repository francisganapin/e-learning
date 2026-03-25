from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # OneToOneField means 1 User can only have exactly 1 Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Basic Profile Info
    bio = models.TextField(blank=True, null=True, help_text="Tell us about yourself!")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # We can track what type of user they are
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
