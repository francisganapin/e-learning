from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Role Constants
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
        (ADMIN, 'Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # New Role System
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    
    # Basic Info
    bio = models.TextField(blank=True, null=True, help_text="Tell us about yourself!")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Communication and Social
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Python Developer")

    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    
    # Gamification
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s ({self.role}) Profile"

# --- SIGNALS ---
# Automatically create a Profile when a new User is registered
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


