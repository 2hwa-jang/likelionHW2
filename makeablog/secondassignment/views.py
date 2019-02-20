from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogPost

# Create your views here.
def home(request):
    blogs = Blog.objects
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs' : blogs, 'posts':posts })

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk = blog_id)
    #blog_id번째 블로그 객체
    return render(request, 'detail.html', {'blog':blog_detail})

def new(request): #new.html 띄워주는 함수
    return render(request, 'new.html')

def create(request): #입력받은 내용을 디비에 넣어주는 함수
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/'+str(blog.id))

def blogpost(request):
    #입력된 내용 처리 --> post method
    #빈 페이지를 띄워줌 --> get 방식
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form':form})
