from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('recipe', views.RecipeViewSet, basename='recipe')
router.register('comment', views.CommentViewSet, basename='comment')
urlpatterns = [
    path('', include(router.urls))
]
