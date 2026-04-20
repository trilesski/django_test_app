from rest_framework.routers import DefaultRouter
from .views import SurveyViewSet, PassSurveyViewSet

router = DefaultRouter()

router.register(r'surveys', SurveyViewSet, basename='surveys')
router.register(r'pass_surveys', PassSurveyViewSet, basename='pass_surveys')

urlpatterns = router.urls
