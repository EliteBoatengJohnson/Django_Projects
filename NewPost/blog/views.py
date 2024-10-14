from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method =='POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fileds passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri( post.get_absolute_url())
            subject =()
    else:
        form =EmailPostForm()
    return render(
        request, 'blog/post/share.html',
        {
            'post': post,
            'form': form
        }
    )

def post_list(request):
    post_list = Post.published.all()
    # pignation with 3 posts per page
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request, 'blog/post/list.html',{'posts':posts}
    )


def post_detail(request,year,month,day,post):
    try:
        post = get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,publish__month=month,publish__day=day)
    except Post.DoesNotExist:
        raise Http404("No Post Found")
    return render (
        request,
        'blog/post/detail.html', 
        {'post':post}
    )