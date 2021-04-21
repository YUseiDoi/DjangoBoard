from django.shortcuts import render, redirect
from django.views.generic import (
        CreateView, FormView, DetailView, TemplateView, ListView)
from . forms import TopicCreateForm
from . models import Topic, Category
from . forms import TopicModelForm, TopicForm, TopicCreateForm, CommentModelForm, Comment
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404



class TopicDetailView(DetailView):
    template_name = 'thread/detail_topic.html'
    model = Topic
    context_object_name = 'topic'


class TopicFormView(FormView):
    template_name = 'thread/create_topic.html'
    form_class = TopicCreateForm
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TopicCreateView(CreateView):
    template_name = 'thread/create_topic.html'
    form_class = TopicModelForm
    model = Topic
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'thread/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'thread/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))    

def topic_create(request):
    template_name = 'thread/create_topic.html'
    ctx = {}
    if request.method == 'GET':
        form = TopicForm()
        ctx['form'] = form
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            # topic_form.save()
            topic = Topic()
            cleaned_data = topic_form.cleaned_data
            topic.title = cleaned_data['title']
            topic.message = cleaned_data['message']
            topic.user_name = cleaned_data['user_name']
            topic.category = cleaned_data['category']
            topic.save()            
            return redirect(reverse_lazy('base:top'))
        else:
            ctx['form'] = topic_form
            return render(request, template_name, ctx)


class CategoryView(ListView):
    template_name = 'thread/category.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Topic.objects.filter(category__url_code = self.kwargs['url_code'])
     
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(Category, url_code=self.kwargs['url_code'])
        return ctx
    

class TopicAndCommentView(FormView):
    template_name = 'thread/detail_topic.html'
    form_class = CommentModelForm
    
    def form_valid(self, form):
        comment = form.save(commit=False) #保存せずオブジェクト生成する
        comment.topic = Topic.objects.get(id=self.kwargs['pk'])
        comment.no = Comment.objects.filter(topic=self.kwargs['pk']).count() + 1
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread:topic', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(
            topic_id=self.kwargs['pk']).order_by('no')
        return ctx
