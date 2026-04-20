from rest_framework.viewsets import ModelViewSet

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Survey, Question, PassSurvey
from .serializers import SurveySerializer, PassSurveySerializer


class SurveyViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        parameters=[
            OpenApiParameter(name='number', location=OpenApiParameter.QUERY, required=True, type=int, default=1),
        ]
    )
    @action(detail=True, methods=['get'])
    def questions(self, request, pk):
        question_num = int(request.query_params.get('number', 1))

        if not question_num:
            return JsonResponse(
                {'error': 'No question number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = (
            Question.objects.select_related('survey')
            .filter(
                survey_id=int(pk),
                number=question_num
            )
            .order_by('number')
        )

        question = queryset.first()

        if not question:
            return JsonResponse(
                {'error': 'Question does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        answers_options =  list(question.answers_options.values('id', 'number', 'text').order_by('number'))

        return JsonResponse(
            {
                'id': question.id,
                'number': question.number,
                'text': question.text,
                'answers_options': answers_options,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def questions_count(self, request, pk):
        total_cnt = Question.objects.select_related('survey').filter(survey_id=int(pk)).acount()
        return JsonResponse({'total_cnt': total_cnt}, status=status.HTTP_200_OK)


class PassSurveyViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PassSurveySerializer
    queryset = PassSurvey.objects.all()
    http_method_names = ['post', 'get', 'delete']

