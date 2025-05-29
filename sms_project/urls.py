from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet, ClassNameViewSet, StudentClassViewSet, ScheduleViewSet, LocationViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'classnames', ClassNameViewSet)
router.register(r'studentclasses', StudentClassViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
