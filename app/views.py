# Create your views here.
from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.contrib.auth.models import User

from app.models import Post, Comment
from app.serializers import PostListSerializer, CommentListSerializer, CommentValidateSerializer, PostValidateSerializer, UserLoginValidateSerializer, UserRegisterValidateSerializer


@api_view(['GET', 'POST'])
def post_list_views(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        data = PostListSerializer(posts, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        serializer = PostValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'error': serializer.errors
                }
            )
        post = Post.objects.create(
            title=serializer.validated_data['title'],
            text=serializer.validated_data['text'],
        )
    return Response(data={'message': 'created'})


@api_view(['GET'])
def post_item_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound('Ничего не найдено')
    data = PostListSerializer(post, many=False).data
    return Response(data=data)


@api_view(['GET', 'POST'])
@permission_classes(['IsAuthenticated'])
def comment_list_views(request):
    if request.method == 'GET':
        comment = Comment.objects.all()
        data = CommentListSerializer(comment, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        serializer = CommentValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'error': serializer.errors
                }
            )
        text = request.data.get('comment', '')
        Comment.objects.create(text=text)
        return Response(data={'message': 'created'})


@api_view(['GET'])
def comment_item_view(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise NotFound('Ничего не найдено')
    data = CommentListSerializer(comment, many=False).data
    return Response(data=data)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'error',
                    'errors': serializer.errors
                }
            )
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
                print("GET TOKEN")
            except:
                print("CREATE TOKEN")
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(data={'message': 'USER NOT FOUND'})


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'error',
                    'errors': serializer.errors
                }
            )
        User.objects.create_user(
            username=request.data['username'],
            email='symbat@gmail.com',
            password=request.data['password']
        )
        return Response(data={'User created'})
