from django.db import models
from django.db.models.deletion import CASCADE


class Poll(models.Model):
    '''Poll description'''
    name = models.CharField(max_length=250)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'polls'

    def __str__(self):
        return self.name

    def get_questions(self):
        questions = Question.objects.filter(poll=self.pk)
        questions_dic = {}
        for question in questions:
            questions_dic[question.pk] = question.text
        return questions_dic
            

class Question(models.Model):
    '''Questions for polls'''
    QUESTION_TYPE = (
        ('text question', 'text question'),
        ('one variant choice', 'one variant choice'),
        ('plural variants choice', 'plural variants choice  ')
    )

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=100, choices=QUESTION_TYPE, default='text question')

    class Meta:
        verbose_name_plural = 'questions'

    def __str__(self):
        return self.text


class CustomPoll(models.Model):
    '''Individual polls of users'''
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user_id = models.IntegerField()

    class Meta:
        verbose_name_plural = 'custom polls'

    def __str__(self):
        return str(self.pk)

    
class RespondentAnswer(models.Model):
    '''Respondents' answers '''
    custom_poll_id = models.ForeignKey(CustomPoll, on_delete=CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'respondets\' answers'

    def __str__(self):
        return self.text