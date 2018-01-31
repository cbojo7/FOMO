from django.db import models


class Question(models.Model):
    question_text = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(null=True)
