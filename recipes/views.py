from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Recipe, Comments
from .serializers import RecipeListSerializer, RecipeViewSerializer, RecipeCreateSerializer, CommentsSerializer, CommentsCreateSerializer


def home(request):
    return render(request, 'index.html')


class RecipeViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_classes = {
        'list': RecipeListSerializer,
        'retrieve': RecipeViewSerializer,
        'create': RecipeCreateSerializer
    }

    def get_queryset(self):
        if self.action == 'retrieve':
            return Recipe.objects.prefetch_related('ingredients_set', 'steps_set')
        else:
            return Recipe.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, RecipeListSerializer)


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_classes = {
        'create': CommentsCreateSerializer
    }
    queryset = Comments.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, CommentsSerializer)
