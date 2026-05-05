from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Project, ProjectReview, ProjectRating, Favorite
from .forms import ProjectForm, ProjectReviewForm, ProjectRatingForm
from .repositories import ProjectRepository
from accounts.mixins import RoleRequiredMixin

class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'
    context_object_name = 'all_projects'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = ProjectRepository() 

    def get_queryset(self):
        return self.repo.get_all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['my_projects'] = self.repo.get_by_creator(profile)
            context['favorited_projects'] = self.repo.get_favorited_by(profile)
            context['reviewed_projects'] = self.repo.get_reviewed_by(profile)
            
            excluded_ids = (
                list(context['my_projects'].values_list('id', flat=True)) +
                list(context['favorited_projects'].values_list('id', flat=True)) +
                list(context['reviewed_projects'].values_list('id', flat=True))
            )
            context['all_projects'] = self.repo.get_all_except(excluded_ids)
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'
    context_object_name = 'project'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = ProjectRepository()

    def get_object(self):
        return self.repo.get_by_id(self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        ratings = project.ratings.all()
        context['average_rating'] = sum(r.score for r in ratings) / ratings.count() if ratings.exists() else 0
        context['favorite_count'] = project.favorites.count()
        
        if self.request.user.is_authenticated:
            context['review_form'] = ProjectReviewForm()
            context['rating_form'] = ProjectRatingForm()
            context['is_favorited'] = project.favorites.filter(profile=self.request.user.profile).exists()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        project = self.get_object()
        profile = request.user.profile

        if 'submit_review' in request.POST:
            form = ProjectReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.project = project
                review.reviewer = profile
                review.save()
        
        elif 'submit_rating' in request.POST:
            form = ProjectRatingForm(request.POST)
            if form.is_valid():
                rating, created = ProjectRating.objects.update_or_create(
                    project=project, profile=profile,
                    defaults={'score': form.cleaned_data['score']}
                )

        elif 'toggle_favorite' in request.POST:
            favorite = Favorite.objects.filter(project=project, profile=profile)
            if favorite.exists():
                favorite.delete()
            else:
                Favorite.objects.create(project=project, profile=profile)

        return redirect('diyprojects:project_detail', pk=project.pk)

class ProjectCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'diyprojects/project_create.html'
    required_role = "Project Creator"

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'diyprojects/project_update.html'
    required_role = "Project Creator"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = ProjectRepository()

    def get_object(self):
        project = self.repo.get_by_id(self.kwargs.get('pk'))
        if project.creator != self.request.user.profile:
            raise PermissionDenied
        return project