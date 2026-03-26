Your models are already quite solid—this is a good foundation for an LMS. But there are a few **critical issues**, plus several **design improvements** that will make your system more scalable and correct.

---

# 🚨 Critical Issues (Must Fix)

## 1. ❌ `UserLessonProgress.is_done` recursion bug

You defined a field and a property with the same name:

```python
is_done = models.BooleanField(default=False)

@property
def is_done(self):
    return self.is_done
```

👉 This creates **infinite recursion** (it keeps calling itself).

### ✅ Fix:

Just remove the property:

```python
is_done = models.BooleanField(default=False)
```

---

## 2. ❌ Lesson completion is incorrectly global

In `Module.completion_percentage`:

```python
done = self.lessons.filter(is_done=True).count()
```

👉 Problem:

* `Lesson` has **no `is_done` field**
* Progress is stored in `UserLessonProgress`
* Completion must be **per user**, not global

---

### ✅ Fix:

Pass `user` into the method:

```python
def completion_percentage(self, user):
    total = self.lessons.count()
    if total == 0:
        return 0

    done = UserLessonProgress.objects.filter(
        user=user,
        lesson__module=self,
        is_done=True
    ).count()

    return int((done / total) * 100)
```

---

## 3. ❌ `Module.is_finished()` logic is wrong

You're using:

```python
self.lessons.filter(is_done=True)
```

Again, ❌ **wrong model**

---

### ✅ Fix:

```python
def is_finished(self, user):
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
```

---

# ⚠️ Design Improvements

## 4. 🔥 Add Unique Constraint for User Progress

Prevent duplicate progress rows:

```python
class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'lesson')
```

---

## 5. 🔥 Use Custom User Model (Best Practice)

Instead of:

```python
from django.contrib.auth.models import User
```

👉 Use:

```python
from django.conf import settings
settings.AUTH_USER_MODEL
```

Example:

```python
instructor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
```

---

## 6. 🔥 Add Indexes for Performance

You will query these frequently:

```python
class QuizResult(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user', 'quiz']),
        ]
```

---

## 7. 🔥 Improve `number_of_try`

Right now:

```python
number_of_try = models.IntegerField(default=0)
```

👉 This is global per quiz, which is incorrect.

### ✅ Better:

Track per user:

```python
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempt_number = models.IntegerField()
```

---

## 8. 🔥 Add ordering consistency

Some models have `order`, some don’t.

Consider:

* Add ordering to `Course`, `Quiz`, etc.
* Or remove if unnecessary

---

## 9. 🔥 Slug auto-generation (quality of life)

Right now you must manually set slugs.

Add:

```python
from django.utils.text import slugify

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
```

---

## 10. 🔥 Media organization

Better structure:

```python
upload_to='courses/%Y/%m/%d/'
upload_to='lessons/%Y/%m/%d/'
```

---

## 11. 🔥 Decimal precision improvement

```python
percentage = models.DecimalField(max_digits=5, decimal_places=2)
```

👉 OK, but you could also compute it dynamically instead of storing it.

---

# 🧠 Architecture Suggestions (Next Level)

## ✅ Add Enrollment Model

Right now, anyone can access courses.

```python
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
```

---

## ✅ Add Course Progress

Instead of computing every time:

```python
class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
```

---

## ✅ Add Certificates (optional)

```python
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
```

---

# 🧾 Summary

### ❌ Major Problems

* Recursive `is_done` property ❗
* Wrong lesson completion logic ❗
* Progress not user-based ❗

### ⚠️ Medium Issues

* No unique constraint
* Weak quiz attempt tracking
* Slug handling manual

### 🚀 Improvements

* Enrollment system
* Performance indexes
* Custom user model
* Better architecture separation

---

# 💬 Final Thought

You're **very close to a production-ready LMS**, but the biggest conceptual fix is:

> 👉 **Everything related to progress must be USER-SPECIFIC, not global.**

---

If you want, I can:

* Refactor this into a **clean production-grade version**
* Add **API (DRF) structure**
* Or build **frontend flow (React / templates)**
