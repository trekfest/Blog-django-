from django.utils import timezone
from django.http import  Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from .models import Article, Category, UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CreationUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from .forms import ArticleForm
from .forms import UserProfileForm

from django.shortcuts import render, get_object_or_404
from .models import Article

def homepage(request):
    return render(request, 'homepage.html')

from .models import Category

def index(request):
    all_articles_list = Article.objects.all()
    categories = Category.objects.all()  # Fetch all categories
    print(categories)
    category_filter = request.GET.get('category')
    if category_filter:
        all_articles_list = all_articles_list.filter(category__name=category_filter)
    return render(request, 'articles/list.html', {'all_articles_list': all_articles_list, 'categories': categories})




def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    latest_comments_list = article.comment_set.order_by('-id')[:10]
    return render(request, 'articles/detail.html', {'article': article, 'latest_comments_list': latest_comments_list})




@login_required
def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404("Article wasn't found")

    if request.method == 'POST':
        csrf_token = request.POST.get('csrfmiddlewaretoken', '')
        if not csrf_token:
            # Handle the case where CSRF token is missing
            return HttpResponseForbidden("CSRF token missing.")

        a.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

        return HttpResponseRedirect(reverse('articles:detail', args=(a.id,)))
    else:
        
        return HttpResponseBadRequest("Invalid request method.")




def register(request):
    if request.method == 'POST':
        form = CreationUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = CreationUser()

    return render(request=request, template_name="registration/register.html", context={"form": form})





@login_required
def profile(request):
    user_profile = request.user.userprofile
    user_articles = Article.objects.filter(author=request.user).order_by('-pub_date')
    return render(request, 'articles/profile.html', {'user_profile': user_profile, 'user_articles': user_articles}, )



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)




@login_required
def update_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user profile page
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'articles/update_profile.html', {'form': form})



@login_required
def user_create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.pub_date = timezone.now()
            article.save()
            return redirect('profile')  
    else:
        form = ArticleForm()
    return render(request, 'registration/user_creation_article.html', {'form': form})



@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    # Verify that the logged-in user owns the article
    if request.user == article.author and request.method == 'POST':
        article.delete()
        return redirect('profile')  

   
    return redirect('profile')