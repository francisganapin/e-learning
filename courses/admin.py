from django.contrib import admin
from .models import Category, Course, Module, Lesson, Quiz, Question, Choice
import nested_admin

# --- 1. ADMIN INLINES (Nested management) ---

class ChoiceInline(nested_admin.NestedStackedInline):
    model = Choice
    extra = 3

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

class LessonInline(nested_admin.NestedStackedInline):
    model = Lesson
    extra = 2
    sortable_options = {'handle': '.drag-handle'}
    prepopulated_fields = {'slug': ('title',)}

class QuizInline(nested_admin.NestedStackedInline):
    model = Quiz
    extra = 1
    inlines = [QuestionInline]
    sortable_options = {'handle': '.drag-handle'}
    prepopulated_fields = {'slug': ('title',)}
    

class LessonInline(nested_admin.NestedStackedInline):
    model = Lesson
    extra = 1
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(nested_admin.NestedStackedInline):
    model = Module
    extra = 1

    inlines = [LessonInline, QuizInline] 

# --- 2. PROFESSIONAL ADMIN SETTINGS ---

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', 'category', 'instructor', 'created_at']
    list_filter = ['created_at', 'category']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    
    # This is the entry point—it nesting everything together
    inlines = [ModuleInline] 
# 3. Simple registration for other things

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
# 4. Optional: Keep standalone Module/Lesson editors for global search

admin.site.register(Module)
admin.site.register(Lesson)