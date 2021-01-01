from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter,OrderingFilter

from django.contrib.auth.models import User
from blog.models import Blog
from blog.api.serializers import BlogSerializer,RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_view(request,pk):

    try:
        blog = Blog.objects.get(pk=pk)

    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_view(request,pk):

        try:
            blog = Blog.objects.get(pk=pk)

        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if blog.author != user:
            return Response({'response':'You are not authorized to edit this post'})

        if request.method == 'PUT':
            serializer = BlogSerializer(blog,data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['success']='update successful'
                return Response(data=data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_view(request,pk):

        try:
            blog = Blog.objects.get(pk=pk)

        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if blog.author != user:
            return Response({'response':'You are not authorized to delete this post'})

        if request.method == 'DELETE':
            operation = blog.delete()
            data = {}
            if operation:
                data['success']='delete successful'
            else:
                data['failure']='delete failed'

            return Response(data=data)

@api_view(['POST',])
def api_create_view(request):
    u=User.objects.get(id=request.user.id)
    blog = Blog(author=u)

    if request.method == 'POST':
        serializer = BlogSerializer(blog,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def register_view(request):

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response']='successfully registered a new user'
            data['email']=user.email
            data['username']=user.username
            token = Token.objects.get(user=user).key
            data['token']=token
        else:
            data = serializer.errors

        return Response(data)

class APIListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','text','author__username')
