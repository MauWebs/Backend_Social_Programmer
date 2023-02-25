from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlogSerializer
from .models import Blog, Comment
from users.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlogs(request):
    blog = Blog.objects.filter().order_by('-date')
    serializer = BlogSerializer(blog, many=True)
    return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSoloBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postBlog(request):
    data = request.data
    blog = Blog.objects.create(
        user=request.user,
        body=data['body'],
    )
    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def putBlog(request, pk):
    data = request.data
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(instance=blog, data=data)
    if blog.user == request.user:
        if serializer.is_valid():
            serializer.save()
    else:
        return Response({'Error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, headers={'Access-Control-Allow-Origin': '*'})
    return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    if blog.user == request.user:
        blog.delete()
        return Response('Blog Eliminado', headers={'Access-Control-Allow-Origin': '*'})
    else:
        return Response({'Error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if comment.user == request.user:
        comment.delete()
        return Response('Comentario Eliminado', headers={'Access-Control-Allow-Origin': '*'})
    else:
        return Response({'Error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, headers={'Access-Control-Allow-Origin': '*'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, pk):
    blog = Blog.objects.get(id=pk)
    user = request.user
    data = request.data
    comment = Comment.objects.create(
        user=user,
        blog=blog,
        text=data['text']
    )
    comments = blog.comment_set.all()
    blog.save()
    return Response('Comentario Añadido', headers={'Access-Control-Allow-Origin': '*'})
