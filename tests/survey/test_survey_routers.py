import pytest
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from apps.survey.models import *
from tests.factories.survey import SurveyFactory, QuestionFactory, AnswerOptionFactory


pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.clickhouse]


class SurveyRoutersTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        # Apply the token to all future requests from this client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get(self):
        survey = SurveyFactory(name='Survey 1', author=self.user)

        question_1 = QuestionFactory(text='Question 1', number=1, survey=survey)
        q1_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_1)
        q1_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_1)
        q1_a3  =AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_1)

        question_2 = QuestionFactory(text='Question 2', number=2, survey=survey)
        q2_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_2)
        q2_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_2)
        q2_a3 = AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_2)

        # Get Survey
        response = self.client.get(reverse('surveys-detail', kwargs={'pk': survey.id}), format='json')
        self.assertEqual(response.status_code, 200)

        data= response.json()

        assert data == {
            'id': survey.id,
            'name': 'Survey 1',
            'questions': [
                {
                    'id': question_1.id,
                    'number': 1,
                    'text': 'Question 1',
                    'answers_options': [
                        {'id': q1_a1.id, 'number': 1, 'text': 'AnswerOption 1'},
                        {'id': q1_a2.id, 'number': 2, 'text': 'AnswerOption 2'},
                        {'id': q1_a3.id, 'number': 3, 'text': 'AnswerOption 3'}
                    ]
                },
                {
                    'id': question_2.id,
                    'number': 2,
                    'text': 'Question 2',
                    'answers_options': [
                        {'id': q2_a1.id, 'number': 1, 'text': 'AnswerOption 1'},
                        {'id': q2_a2.id, 'number': 2, 'text': 'AnswerOption 2'},
                        {'id': q2_a3.id, 'number': 3, 'text': 'AnswerOption 3'}
                    ]
                }
            ]
        }

        # Get servey questions 1
        response = self.client.get(reverse('surveys-questions', kwargs={'pk': survey.id}), format='json')
        self.assertEqual(response.status_code, 200)

        data= response.json()

        assert data == {
            'id': question_1.id,
            'number': 1,
            'text': 'Question 1',
            'answers_options': [
                {'id': q1_a1.id, 'number': 1, 'text': 'AnswerOption 1'},
                {'id': q1_a2.id, 'number': 2, 'text': 'AnswerOption 2'},
                {'id': q1_a3.id, 'number': 3, 'text': 'AnswerOption 3'}
            ]
        }

        # Get servey questions 2
        response = self.client.get(reverse('surveys-questions', kwargs={'pk': survey.id}, query={'number': 2}), format='json')
        self.assertEqual(response.status_code, 200)

        data= response.json()

        assert data == {
            'id': question_2.id,
            'number': 2,
            'text': 'Question 2',
            'answers_options': [
                {'id': q2_a1.id, 'number': 1, 'text': 'AnswerOption 1'},
                {'id': q2_a2.id, 'number': 2, 'text': 'AnswerOption 2'},
                {'id': q2_a3.id, 'number': 3, 'text': 'AnswerOption 3'}
            ]
        }

    def test_delete(self):
        survey = SurveyFactory(name='Survey 1', author=self.user)

        question_1 = QuestionFactory(text='Question 1', number=1, survey=survey)
        q1_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_1)
        q1_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_1)
        q1_a3 = AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_1)

        question_2 = QuestionFactory(text='Question 2', number=2, survey=survey)
        q2_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_2)
        q2_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_2)
        q2_a3 = AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_2)


        response = self.client.delete(reverse('surveys-detail', kwargs={'pk': survey.id}), format='json')
        self.assertEqual(response.status_code, 204)

        assert Survey.objects.filter(pk=survey.id).first() is None

        assert Question.objects.filter(pk=question_1.id).first() is None
        assert AnswerOption.objects.filter(pk=q1_a1.id).first() is None
        assert AnswerOption.objects.filter(pk=q1_a2.id).first() is None
        assert AnswerOption.objects.filter(pk=q1_a3.id).first() is None

        assert Question.objects.filter(pk=question_2.id).first() is None
        assert AnswerOption.objects.filter(pk=q2_a1.id).first() is None
        assert AnswerOption.objects.filter(pk=q2_a2.id).first() is None
        assert AnswerOption.objects.filter(pk=q2_a3.id).first() is None

    def test_update(self):
        survey = SurveyFactory(name='Survey 1', author=self.user)

        question_1 = QuestionFactory(text='Question 1', number=1, survey=survey)
        q1_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_1)
        q1_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_1)
        q1_a3 = AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_1)

        question_2 = QuestionFactory(text='Question 2', number=2, survey=survey)
        q2_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_2)
        q2_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_2)
        q2_a3 = AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_2)

        # Get Survey
        data = {
            'name': 'New Survey 1',
            'questions': [
                {
                    'number': 1,
                    'text': 'Question 11',
                    'answers_options': [
                        {'number': 1, 'text': 'AnswerOption 1'},
                        { 'number': 2, 'text': 'AnswerOption 22'},
                        { 'number': 3, 'text': 'AnswerOption 3'}
                    ]
                },
                {
                    'number': 2,
                    'text': 'Question 2',
                    'answers_options': [
                        {'number': 1, 'text': 'AnswerOption 1'},
                        {'number': 2, 'text': 'AnswerOption 2'},
                        {'number': 3, 'text': 'AnswerOption 3'}
                    ]
                }
            ]
        }

        response = self.client.put(reverse('surveys-detail', kwargs={'pk': survey.id}), data=data, format='json')
        self.assertEqual(response.status_code, 200)

        data= response.json()

        assert data['name'] == 'New Survey 1'
        assert data['questions'][0]['text'] == 'Question 11'
        assert data['questions'][0]['answers_options'][1]['text'] == 'AnswerOption 22'

    def test_pass_surveys_create(self):
        survey = SurveyFactory(name='Survey 1', author=self.user)
        survey2 = SurveyFactory(name='Survey 2', author=self.user)

        question_101 = QuestionFactory(text='Question 101', number=1, survey=survey2)
        ao_101 = AnswerOptionFactory(text='AnswerOption 101', number=1, question=question_101)

        question_1 = QuestionFactory(text='Question 1', number=1, survey=survey)
        q1_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_1)
        q1_a2 = AnswerOptionFactory(text='AnswerOption 2', number=2, question=question_1)
        q1_a3 = AnswerOptionFactory(text='AnswerOption 3', number=3, question=question_1)

        question_2 = QuestionFactory(text='Question 2', number=2, survey=survey)
        q2_a1 = AnswerOptionFactory(text='AnswerOption 1', number=1, question=question_2)

        data = {
            "survey": survey.id,
            "user_answers": [
                {
                    "question": question_1.id,
                    "answer_option": q1_a2.id,
                    "user_option": ""
                },
                {
                    "question": question_2.id,
                    "answer_option": None,
                    "user_option": "My answer"
                }
            ],
            "started_at": "2026-04-20T06:52:59.548Z",
            "finished_at": "2026-04-20T06:52:59.548Z"
        }

        response = self.client.post(reverse('pass_surveys-list'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        assert response_data['survey'] == survey.id
        assert response_data['user_answers'][0]['question'] == question_1.id
        assert response_data['user_answers'][0]['answer_option'] == q1_a2.id
        assert response_data['user_answers'][0]['user_option'] == ''

        assert response_data['user_answers'][1]['question'] == question_2.id
        assert response_data['user_answers'][1]['answer_option'] is None
        assert response_data['user_answers'][1]['user_option'] == 'My answer'


        # Incorrect 'answer_option' exception
        data['user_answers'][0]['answer_option'] = ao_101.id

        response = self.client.post(reverse('pass_surveys-list'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

        response_data= response.json()
        assert response_data == {'user_answers': ["Incorrect 'answer_option' was passed"]}

        # Incorrect 'question' exception
        data['user_answers'][0]['question'] = question_101.id

        response = self.client.post(reverse('pass_surveys-list'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

        response_data= response.json()
        assert response_data == {'user_answers': ["Incorrect 'question' was passed"]}