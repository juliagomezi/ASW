from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.template.defaultfilters import register

from django.views.generic import TemplateView

from HackerNews.models import Comment, Contribution, UserDetail, SubmitForm, ContributionVote

from django.contrib.auth.models import User


def vote(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            id = request.POST.get('id')
            contribution = Contribution.objects.get(id=id)
            contribution.points = contribution.points + 1
            contribution.save()
            contributionvote = ContributionVote()
            contributionvote.user = request.user
            contributionvote.contribution = contribution
            contributionvote.save()
        else:
            return redirect('/login')
    return redirect(request.POST.get('next'))


def unvote(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            contribution = Contribution.objects.get(id=id)
            contribution.points = contribution.points - 1
            contribution.save()
            ContributionVote.object.get(user=request.user, contribution=contribution).delete()
        else:
            return redirect('/login')
    return redirect('/')


def index(request):
    votes = None
    if request.user.is_authenticated:
        votes = ContributionVote.objects.filter(user=request.user).values_list('contribution', flat=True)
    return render(request, "news.html", {
        "contributions": Contribution.objects.all().order_by('-points'),
        "submit": False,
        "votes": votes

    })


def newest(request):
    votes = None
    if request.user.is_authenticated:
        votes = ContributionVote.objects.filter(user=request.user)
    return render(request, "news.html", {
        "contributions": Contribution.objects.all().order_by('-date'),
        "submit": False,
        "selected": "newest",
        "votes": votes
    })


def threads(request):
    return render(request, "news.html", {
        "contributions": Contribution.objects.all(),
        "submit": False,
        "selected": "threads"
    })


def ask(request):
    votes = None
    if request.user.is_authenticated:
        votes = ContributionVote.objects.filter(user=request.user).values_list('contribution', flat=True)
    return render(request, "news.html", {
        "contributions": Contribution.objects.filter(type="ask").order_by('-points'),
        "submit": False,
        "selected": "ask",
        "votes": votes
    })


def profile(request, id):
    return render(request, "profile.html", {
        "profile": User.objects.get(id=id),
        "profileDetails": UserDetail.objects.get(id=id),
        "submit": False
    })


comments = []
fathers = []


def item(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comment()
            comment.contribution = Contribution.objects.get(id=request.POST.get('contribution'))
            comment.text = request.POST.get('text')
            comment.author = request.user
            level = request.POST.get('level')
            comment.level = level
            if level != 0:
                comment.father = request.POST.get('father')
            comment.save()
            return redirect('/item/' + str(request.POST.get('contribution')))
        else:
            return redirect('/login')

    fathers = Comment.objects.filter(contribution=Contribution.objects.get(id=id)).filter(level=0)
    comments = []

    for com in fathers:
        comments.append(com)
        orderComments(1, com, comments, id)

    return render(request, "comment.html", {
        "contribution": Contribution.objects.get(id=id),
        "comments": comments
    })


def updateProfile(request, id):
    if request.method == 'POST':
        comment = Comment()
        comment.contribution = Contribution.objects.get(id=request.POST.get('contribution'))
        comment.text = request.POST.get('text')
        level = request.POST.get('level')
        comment.level = level
        if level != 0:
            comment.father = request.POST.get('father')

        comment.save()
        return redirect('/item/' + str(request.POST.get('contribution')))

    fathers = Comment.objects.filter(contribution=Contribution.objects.get(id=id)).filter(level=0)
    comments = []

    for com in fathers:
        comments.append(com)
        orderComments(1, com, comments, id)

    return render(request, "comment.html", {
        "contribution": Contribution.objects.get(id=id),
        "comments": comments
    })


def orderComments(i, father, comments, id):
    children = Comment.objects.filter(contribution=Contribution.objects.get(id=id)).filter(level=i).filter(
        father=father)
    for child in children:
        gchildren = Comment.objects.filter(contribution=Contribution.objects.get(id=id)).filter(level=i + 1).filter(
            father=child)

        if len(gchildren) == 0:
            comments.append(child)
        else:
            comments.append(child)
            orderComments(i + 1, child, comments, id)


def reply(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        if len(request.POST.get('text')) == 0:
            return errormessage(request)
        father = Comment.objects.get(id=request.POST.get('father'))
        comment = Comment()
        comment.text = request.POST.get('text')
        comment.father = father
        comment.level = father.level + 1
        comment.contribution = father.contribution
        comment.author = request.user
        comment.save()
        return redirect('/item/' + str(father.contribution.id))
    return render(request, "reply.html", {
        "comment": Comment.objects.get(id=id)
    })


class SubmitView(TemplateView):
    template_name = "submit.html"

    def get(self, request):
        form = SubmitForm
        if request.user.is_authenticated:
            return render(request, self.template_name, {"form": form, "submit": True})
        return redirect('/login')

    def post(self, request):
        form = SubmitForm(request.POST)
        url = request.POST.get('url')
        if form.is_valid():
            c = Contribution()
            c.title = request.POST.get('title')
            c.url = request.POST.get('url')
            c.author = request.user
            if not c.url:
                c.text = request.POST.get('text')
                c.type = 'ask'
            else:
                match = Contribution.objects.filter(url=url).exists()
                if match:
                    return redirect('../item/' + str(Contribution.objects.get(url=url).id))
            c.save()
            if request.POST.get('url') and request.POST.get('text'):
                com = Comment()
                com.text = request.POST.get('text')
                com.contribution = Contribution.objects.get(url=c.url)
                com.save()
            return redirect('/')
        return errormessage(request)


def errormessage(request):
    return render(request, "message.html")


def signout(request):
    logout(request)
    return redirect('/')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):

        creationForm = UserCreationForm(prefix='creation')
        creationForm.fields['username'].required = False
        creationForm.fields['password1'].required = False
        creationForm.fields['password2'].required = False
        loginForm = AuthenticationForm(prefix='login')
        loginForm.fields['username'].required = False
        loginForm.fields['password'].required = False

        return self.render_to_response(
            {'c_form': creationForm, 'a_form': loginForm})

    def post(self, request, *args, **kwargs):
        creationForm = UserCreationForm(request.POST, prefix='creation')
        form = AuthenticationForm(request.POST, prefix='login')
        if 'creation' in request.POST and creationForm.is_bound and creationForm.is_valid():
            creationForm.save()
            user = creationForm.cleaned_data['username']
            password = creationForm.cleaned_data['password1']
            user = authenticate(request, username=user, password=password)
            login(request, user)
            return redirect('/')
        elif 'login' in request.POST:
            username = request.POST['login-username']
            password = request.POST['login-password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

        return self.render_to_response({'c_form': creationForm, 'a_form': AuthenticationForm(prefix='login')})


def createuser(request):
    if not UserDetail.objects.filter(user=request.user).exists():
        userDetails = UserDetail(user=request.user)
        userDetails.save()
    return redirect('/')


@register.filter
def in_category(things, contribution):
    return things.filter(contribution=contribution)
