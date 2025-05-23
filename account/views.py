from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import LoginForm


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        # on lie le formulaire aux donnees soumises
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            # Récupère le dictionnaire des données validées et nettoyées.
            cd = form.cleaned_data
            print(cd)
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']          
            )
            if user is not None:
                if user.is_active:
                    # la fonction login fais plusieurs choses :
                    # 1. Elle stocke l'ID de l'utilisateur (user.id) dans la session du request
                    # 2. Le "middleware" de session de Django (SessionMiddleware) s'assure que cet ID est sauvegardé (par défaut dans la base de données, table django_session). Un cookie de session est envoyé au navigateur de l'utilisateur pour identifier cette session lors des requêtes suivantes.
                    # 3. Le "middleware" d'authentification (AuthenticationMiddleware) utilisera cet ID de session lors des prochaines requêtes pour récupérer l'objet User correspondant et l'attacher à request.user. C'est ainsi que Django "sait" qui est connecté sur les pages suivantes.
                    # 4. Elle effectue une rotation de la clé de session pour des raisons de sécurité (prévention de la fixation de session).
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
            
                
