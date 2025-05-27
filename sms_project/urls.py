from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet, ClassNameViewSet, StudentClassViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'classnames', ClassNameViewSet)
router.register(r'studentclasses', StudentClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
