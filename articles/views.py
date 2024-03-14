from django.utils import timezone
from django.http import Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from .models import Article, ArticleView, Category, UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth import login
from .forms import CreationUser, ArticleForm, UserProfileForm  
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def homepage(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'homepage.html', {'latest_articles_list': latest_articles_list})


def index(request):
    all_articles_list = Article.objects.all()
    categories = Category.objects.all().order_by('name')
    category_filter = request.GET.get('category')
    if category_filter:
        all_articles_list = all_articles_list.filter(category__name=category_filter)
        print(f"Category filter applied: {category_filter}")

    # Store the filtered articles in a variable
    filtered_records = all_articles_list

    # Sorting articles based on the provided sorting parameter
    sort_by = request.GET.get('sort')
    if sort_by == 'newest':
        filtered_records = filtered_records.order_by('-pub_date')
        print("Sorting by newest")
    elif sort_by == 'oldest':
        filtered_records = filtered_records.order_by('pub_date')
        print("Sorting by oldest")

    

    return render(request, 'articles/list.html', {'all_articles_list': filtered_records, 'categories': categories})





def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    # Increment the views_count for this article and user
    if request.user.is_authenticated:
        article_view, created = ArticleView.objects.get_or_create(user=request.user, article=article)
        if created:
            article_view.views_count += 1
            article_view.save()
    
    latest_comments_list = article.comment_set.order_by('-id')[:10]
    views_count = article.articleview_set.aggregate(Sum('views_count'))['views_count__sum']
    
    return render(request, 'articles/detail.html', {'article': article, 'latest_comments_list': latest_comments_list, 'views_count': views_count})






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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Save the form without committing to access the profile image
            user_profile = form.save(commit=False)
            if user_profile.profile_image:
                # If a new image is uploaded, save the profile and create the directory if needed
                user_profile.save()
                if not os.path.exists(user_profile.profile_image.path):
                    os.makedirs(user_profile.profile_image.path)
            else:
                # If no new image is uploaded, save the profile directly
                user_profile.save()
            return redirect('profile')
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