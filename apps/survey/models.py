from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from django.db import models


User = get_user_model()


class Survey(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    author = models.ForeignKey(User, verbose_name='Автор', related_name='surveys', on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now_add=True)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.name


class Question(models.Model):
    survey = models.ForeignKey('Survey', related_name='questions', on_delete=models.CASCADE)

    number = models.PositiveIntegerField(verbose_name='Номер вопроса', validators=[MinValueValidator(1)])
    text = models.CharField(verbose_name='Текст вопроса', max_length=256)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now_add=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        unique_together = ('survey', 'number')

    def __str__(self):
        return f'Survey: {self.survey} - Question: {self.text}'


class AnswerOption(models.Model):
    question = models.ForeignKey('Question', related_name='answers_options', on_delete=models.CASCADE)

    number = models.PositiveIntegerField(verbose_name='Номер ответа',  validators=[MinValueValidator(1)])
    text = models.CharField(verbose_name='Текст ответа', max_length=256)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now_add=True)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        unique_together = ('number', 'question')

    def __str__(self):
        return f'Question: {self.question} - Answer options: {self.text}'


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_option = models.ForeignKey('AnswerOption', on_delete=models.CASCADE, null=True, blank=True)

    user_option = models.CharField(verbose_name='Пользовательский вариант', max_length=256, blank=True)

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        return f'Question: {self.question} - User answer: {self.pk}'


class PassSurvey(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    survey = models.ForeignKey(
        'Survey',
        verbose_name='Опрос',
        related_name='pass_surveys',
        on_delete=models.CASCADE
    )

    user_answer_ids = ArrayField(models.PositiveIntegerField(), verbose_name='ID Ответов пользователя', default=list)
    is_completed = models.BooleanField(verbose_name='Опрос пройден?', default=False)

    started_at = models.DateTimeField(verbose_name='Дата старта')
    finished_at = models.DateTimeField(verbose_name='Дата завершения', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Прохождение опроса'
        verbose_name_plural = 'Прохождения опросов'

    def __str__(self):
        return f'User: {self.user} - Survey: {self.survey}'

    @property
    def user_answers(self):
        return UserAnswer.objects.filter(pk__in=self.user_answer_ids)