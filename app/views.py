from itertools import count
from django.contrib.auth.models import User
from django.db.models.functions import TruncDate
from django.db.models import Count

import datetime

from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import action

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
    
    # @action(detail=False, methods=['Get'], name='analytics') #?date_from=2020-02-02&date_to=2020-02-15 
    # def analytics(self, request, *args, **kwargs):
    #     queryset = Like.objects.filter(datetime__lte=datetime.datetime(request.query_params.get('date_from'))).filter(datetime__gte=datetime.datetime(request.query_params.get('date_to')))
    #     serializer = LikeSerializer(queryset, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
class AnalyticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeByDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
         return self.queryset.filter(post__author__id=self.request.user.id)\
            .values(day=TruncDate('datetime'))\
                .annotate(
                    count=Count('*')
                )



