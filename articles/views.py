from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.views.generic import ListView,DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy 
from .models import Article
from django.shortcuts import render



class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(DetailView):
    model=Article
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Article
    fields = ('title', 'summary','body','photo',)
    template_name = 'article_edit.html'

    def test_func(self):
        obj=self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article.list')

    def test_func(self):
        obj=self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(UserPassesTestMixin,LoginRequiredMixin,CreateView):
    model = Article
    template_name = 'article_new.html'
    fields=('title','summary','body','photo',)

    def form_valid(self, form) :
        form.instance.author = self.request.user
        return super().form_valid(form)   
    
    def test_func(self) :
        return self.request.user.is_superuser
    
def article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        
        # Access the 'photo' attribute
        photo = article.photo

        if photo and photo.file:
            # File exists, perform desired operations
            return render(request, 'article_detail.html', {'article': article})
        else:
            # File is missing, handle this scenario
            return render(request, 'article_detail.html', {'article': article, 'default_photo': '/path/to/default.jpg'})

    except Article.DoesNotExist:
        # Handle the case where the article does not exist
        return render(request, 'article_not_found.html')
