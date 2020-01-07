from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from django.shortcuts import render, redirect
from .models import Blog
from .serializers import BlogSerializer

# Create your views here.
def all_blogs(request):
    blogs = Blog.objects.all()
    print(blogs)
    return render(request, "all_blogs.html", {"blogs":blogs})

def add_blog(request):
    if request.method == "POST":
        b = Blog()
        b.title = request.POST.get("title")
        b.body = request.POST.get("body")
        b.save()
        return redirect("all_blogs")
    return render(request, "add_blog.html")

@api_view(['GET', 'POST'])
def api_blog_list(request):
    if request.method == 'GET':
        data = Blog.objects.all()

        serializer = BlogSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def api_blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)