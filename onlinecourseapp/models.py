from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=200, default="Online Course")
    description = models.TextField()
    pub_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson Title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.name} - Lesson {self.order}: {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        """
        Determines if the selected choice IDs for this question match the correct choice(s).
        """
        all_correct_ids = set(self.choices.filter(is_correct=True).values_list('id', flat=True))
        selected_ids_set = set(map(int, selected_ids))
        return len(all_correct_ids) > 0 and all_correct_ids == selected_ids_set


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    choices = models.ManyToManyField(Choice, related_name='submissions')
    score = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student = self.user.username if self.user else "Student"
        return f"Submission #{self.id} for {self.course.name if self.course else 'Course'} by {student} ({self.score}/{self.total})"
