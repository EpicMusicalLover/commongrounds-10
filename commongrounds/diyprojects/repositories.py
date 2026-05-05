from .models import Project

class ProjectRepository:
    def get_all(self):
        return Project.objects.all()

    def get_by_category(self, category_name):
        return Project.objects.filter(category__name__iexact=category_name)

    def get_recent(self, n):
        return Project.objects.all()[:n]

    def get_by_id(self, id):
        return Project.objects.get(pk=id)

    def get_by_creator(self, profile):
        return Project.objects.filter(creator=profile)

    def get_favorited_by(self, profile):
        return Project.objects.filter(favorites__profile=profile)

    def get_reviewed_by(self, profile):
        return Project.objects.filter(reviews__reviewer=profile).distinct()
        
    def get_all_except(self, excluded_ids):
        return Project.objects.exclude(id__in=excluded_ids)