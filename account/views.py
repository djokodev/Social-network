from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            password_clair = []
            password_clair.append(user_form.cleaned_data['password'])

            print(password_clair)

            # hach password before save in DB
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {'new_user': new_user})
        
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

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
            
                
