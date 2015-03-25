from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import check_password, make_password

from notdienste.settings import SUPPORT_EMAIL
from services.models import *
from services.util import get_distances
from services.paginator import paginate
from services.text import UNKNOWN_PLZ
# from .forms import CaptchaForm

def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    return render(request, 'index.html', context)

def search(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'category': category
    }

    return render(request, 'services/search.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    try:
        plz = Location.objects.get(plz=request.GET['plz'])

    except:
        context = {
            'error': UNKNOWN_PLZ.format(SUPPORT_EMAIL)
        }
        return render(request, 'error.html', context)

    services = Service.objects.filter(category=category)

    distances = get_distances(plz, services)

    # Put them in a list, so they are sortable, and sort them by
    # distance.
    slist = []
    for service in distances:
        slist += [(distances[service], service)]
    slist.sort()
    servicelist = paginate(slist, 10)

    context = {
        'plz': plz,
        'category': category,
        'distances': distances,
        'servicelist': servicelist
    }

    return render(request, 'services/category.html', context)

def service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    context = {}
    # Contact data was requested, check the captcha.
    # context['contact'] = 0
    # if request.method == 'POST':
    #     form = CaptchaForm(request.POST)
    #     if form.is_valid():
    #         context['contact'] = 1
    # else:
    #     form = CaptchaForm()

    if request.user.is_authenticated():
        try:
            r = Rating.objects.get(by=request.user, of=service)
            context['rating'] = r
        except: # There is no past rating of this user for this service.
            pass
        if 'r' in request.GET:
            rs = int(request.GET['r'])
            try:
                r.stars = rs
            except:
                r = Rating(by=request.user, of=service, stars=rs)
            r.text = request.GET['rt']
            if 6 > rs > 0:
                r.save()
            context['rating'] = r

    ratings = paginate(Rating.objects.filter(of=service).order_by('-at'), 5)

    context['service'] = service
    context['ratings'] = ratings
    # context['form'] = form

    return render(request, 'services/service.html', context)

def manage(request):
    if not request.user.is_authenticated():
        return redirect('/')

    context = {
        'listings': Service.objects.filter(owner=request.user)
    }

    return render(request, 'services/manage.html', context)

def personal_data(request):
    if not request.user.is_authenticated():
        return redirect('/')

    return render(request, 'services/personal_data.html')

def verification(request):
    if not request.user.is_authenticated():
        return redirect('/')

    return render(request, 'services/verification.html')

