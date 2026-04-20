from rest_framework.serializers import ModelSerializer

from django.db import transaction
from rest_framework import serializers

from apps.survey.models import Survey, Question, AnswerOption, PassSurvey, UserAnswer


class AnswerOptionSerializer(ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'number', 'text']


class QuestionSerializer(ModelSerializer):
    answers_options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'number', 'text', 'answers_options']


class SurveySerializer(ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['id', 'name','questions']
        write_only_fields = ['name', 'questions']
        read_only_fields = ['id']

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')

        survey = Survey.objects.create(author=self.context['request'].user, **validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers_options')

            question = Question.objects.create(survey=survey, **question_data)

            to_create_answers = [AnswerOption(question=question, **answer, ) for answer in answers_data]
            AnswerOption.objects.bulk_create(to_create_answers)

        return survey

    def update(self, instance, validated_data):
        instance.delete()
        return self.create(validated_data)

    # TODO: Код ниже как возможное решение partial_update,
    #  но есть сложность с большим кол-вом запросов к базе из-за вложенности объектов
    # @transaction.atomic
    # def partial_update(self, instance, validated_data):
    #     questions_data_map = {
    #         x['text']: {'number': x['number'], 'answers_options': x['answers_options']}
    #         for x in validated_data.pop('questions')
    #     }
    #
    #     instance.author = self.context['request'].user
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #
    #     # Удаляем все questions по text которые не пришли в запросе
    #     instance.questions.exclude(text__in=questions_data_map).delete()
    #
    #     questions = instance.questions.all()
    #
    #     for question in questions:
    #         question_data = questions_data_map.pop(question.text)
    #         answers_options_data_map = {
    #             x['text']: {'number': x['number']}
    #             for x in question_data.pop('answers_options')
    #         }
    #
    #         if question.number != question_data['number']:
    #             question.number = question_data['number']
    #             question.save()
    #
    #         # Удаляем все answers_options по text которые не пришли в запросе
    #         question.answers_options.exclude(text__in=answers_options_data_map).delete()
    #
    #         answers_options = question.answers_options.all()
    #
    #         for answer in answers_options:
    #             answer_data = answers_options_data_map.pop(answer.text)
    #             if answer.number != answer_data['number']:
    #                 answer.number = answer_data['number']
    #                 answer.save()
    #
    #     return instance


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'answer_option', 'user_option']


class PassSurveySerializer(ModelSerializer):
    user_answers = UserAnswerSerializer(many=True)

    class Meta:
        model = PassSurvey
        fields = ['id', 'user', 'survey', 'user_answers', 'started_at', 'finished_at']
        read_only_fields = ['id', 'user']

    def validate_user_answers(self, user_answers):
        question = (
            Question.objects
            .filter(pk__in=[x['question'].id for x in user_answers])
            .values('id', 'survey_id')
        )

        if any(self.initial_data['survey'] != x['survey_id'] for x in question) :
            raise serializers.ValidationError("Incorrect 'question' was passed")

        answer_option_question_ids = (
            AnswerOption.objects
            .filter(pk__in=[x['answer_option'].id for x in user_answers if x['answer_option']])
            .values_list('question', flat=True)
        )

        if not all(x in [x['id'] for x in question] for x in answer_option_question_ids):
            raise serializers.ValidationError("Incorrect 'answer_option' was passed")

        return user_answers

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        user_answers_data = validated_data.pop('user_answers')

        to_user_answer = [UserAnswer(user=user, **user_answer) for user_answer in user_answers_data]
        created_user_answer = UserAnswer.objects.bulk_create(to_user_answer)
        user_answer_ids = [obj.id for obj in created_user_answer]

        question_count = Question.objects.select_related('survey').filter(survey=validated_data['survey'].id).acount()
        is_completed = True if question_count == len(user_answer_ids) else False

        survey = PassSurvey.objects.create(
            user=user,
            user_answer_ids=user_answer_ids,
            is_completed=is_completed,
            **validated_data
        )

        return survey
