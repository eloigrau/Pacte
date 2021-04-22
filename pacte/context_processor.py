from blog.models import Choix

def navbar(request):
    return {'sousgroupesArticles': Choix.sousgroupesArticles, }
