import json
from telnetlib import STATUS
from django.views.generic import View
from requests import Response

from accounts.models import User
from todos.serializers import TodoSerializer
from .models import Todo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action

from rest_framework import permissions, generics, status, mixins, viewsets
from rest_framework.views import APIView

class TodoListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = TodoSerializer

	### GenericAPIView의 get_queryset 메소드를 오버라이드 ###
  def get_queryset(self):
    return Todo.objects.filter(author=self.request.user)
  
  def get(self, request):
    return self.list(request)
  
  def post(self, request):
    return self.create(request)
  
	### CreateModelMixin의 perform_create 메소드를 오버라이드 ###
  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

    ## 커스텀할 기능들에 대해서만 mixin 을 이용해서 재정의, 기본적인 기능들은 Generic APIView 로도 처리가 가능하다.


# class TodoViewSet(viewsets.ModelViewSet):
#   permission_classes = [permissions.IsAuthenticated]
#   serializer_class = TodoSerializer
#   queryset = Todo.objects.all()

#   def get_queryset(self):
#     return Todo.objects.filter(author=self.request.user)
  
#   def perform_create(self, serializer):
#     serializer.save(author=self.request.user)

# 	### 추가하기 ###
#   @action(detail=True, methods=['patch'])
#   def check(self, request, pk):
#     todo = Todo.objects.get(pk=pk)
#     todo.check_todo()
#     serializer = self.serializer_class(todo)
#     return Response(serializer.data, status=status.HTTP_200_OK)