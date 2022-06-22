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
    UserRetrieveSerializer, 
    UserListSerializer, 
    UserActivitySerializer, 
    PostCreateSerializer, 
    PostRetrieveSerializer)

def last_activity_trigger(user):
    user.last_request = datetime.datetime.now()
    user.save(update_fields=['last_request'])
    return

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
            if self.action == 'retrieve':
                return UserRetrieveSerializer
            return UserListSerializer
    
    def get_queryset(self):
        last_activity_trigger(self.request.user)
        return self.queryset

    @action(detail=True, methods=['Get'], name='activity')
    def activity(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserActivitySerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

    def get_queryset(self):
        last_activity_trigger(self.request.user)
        return self.queryset
    
    @action(detail=True, methods=['Get'], name='likes')
    def likes(self, request, *args, **kwargs):
        last_activity_trigger(self.request.user)
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
    
    def get_queryset(self):
        last_activity_trigger(self.request.user)
        return self.queryset

class AnalyticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeByDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = DateFilter

    def get_queryset(self):
        last_activity_trigger(self.request.user)
        return self.queryset.filter(post__author__id=self.request.user.id)\
            .values(day=TruncDate('created_at'))\
                .annotate(
                    count=Count('*')
                )

# class UserActivityViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserActivitySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         serializer = UserActivitySerializer(user)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
