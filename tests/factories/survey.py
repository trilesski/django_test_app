import string

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


class SurveyFactory(DjangoModelFactory):
    class Meta:
        model = 'survey.Survey'

    name = FuzzyText(length=15, chars=string.ascii_letters)
    author = FuzzyText(length=15, chars=string.ascii_letters)


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = 'survey.Question'

    survey = SubFactory(SurveyFactory)

    number = 1
    text = FuzzyText(length=15, chars=string.ascii_letters)


class AnswerOptionFactory(DjangoModelFactory):
    class Meta:
        model = 'survey.AnswerOption'

    question = SubFactory(QuestionFactory)

    number = 1
    text = FuzzyText(length=15, chars=string.ascii_letters)