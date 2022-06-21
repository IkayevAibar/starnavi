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
    
# class DateFilterBackend(DjangoFilterBackend):
#     """
#     Custom status filter for student, doctor orders
#     """

#     def filter_queryset(self, request, queryset, view):
#         date_from = '1999-01-01'
#         date_to = '3000-01-01'
        
#         if(self.request.query_params.get('date_from')):
#             date_from = self.request.query_params.get('date_from').strip()
#         if(self.request.query_params.get('date_to')):
#             date_to = self.request.query_params.get('date_to').strip()
#         else:
#             return queryset
        
#         return queryset

class DateFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter('datetime', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter('datetime', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ['datetime'] 

class AnalyticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeByDaySerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DateFilterBackend]

    filter_backends = (DjangoFilterBackend,)
    filter_class = DateFilter

    def get_queryset(self):
        # date_from = '1999-01-01'
        # date_to = '3000-01-01'
        
        # if(self.request.query_params.get('date_from')):
        #     date_from = self.request.query_params.get('date_from').strip()
        # if(self.request.query_params.get('date_to')):
        #     date_to = self.request.query_params.get('date_to').strip()
        
        # splited_date_from = date_from.split('-')
        # date_from_ = datetime.date(int(splited_date_from[0]),int(splited_date_from[1]),int(splited_date_from[2]))

        # splited_date_to = date_to.split('-')
        # date_to_ = datetime.date(int(splited_date_to[0]),int(splited_date_to[1]),int(splited_date_to[2]))

        return self.queryset.filter(post__author__id=self.request.user.id)\
            .values(day=TruncDate('datetime'))\
                .annotate(
                    count=Count('*')
                )\
                    # .filter({'day__range': \
                    #     (datetime.datetime.combine(date_from_, datetime.time.min),
                    #         datetime.datetime.combine(date_to_, datetime.time.max))})
                    # .filter(day__lte=date_from)\
                    # .filter(day__gte=date_to)




