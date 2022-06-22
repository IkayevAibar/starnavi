from itertools import count
from django.contrib.auth.models import User
from django.db.models.functions import TruncDate
from django.db.models import Count
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

import datetime

from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import action

from .filters import DateFilter
from app.models import Post, Like
from .serializers import (
    LikeByDaySerializer,
    LikeCreateSerializer, 
    LikeSerializer,
    UserSerializer, 
    PostCreateSerializer, 
    PostRetrieveSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Posts to be viewed or created.
    """
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
            if self.action == 'create':
                return PostCreateSerializer
            return PostRetrieveSerializer

    @action(detail=True, methods=['Get'], name='likes')
    def likes(self, request, *args, **kwargs):
        post = self.get_object()
        queryset = Like.objects.filter(post=post)
        serializer = LikeSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Posts to be viewed or created.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
            if self.action == 'create':
                return LikeCreateSerializer
            return LikeSerializer
    

class AnalyticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeByDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = DateFilter

    def get_queryset(self):
        return self.queryset.filter(post__author__id=self.request.user.id)\
            .values(day=TruncDate('created_at'))\
                .annotate(
                    count=Count('*')
                )

