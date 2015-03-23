from django.shortcuts import render, get_object_or_404

from notdienste.settings import SUPPORT_EMAIL
from services.models import *
from services.util import get_distances
from services.payments import create_payment
from services.paginator import paginate
from services.text import UNKNOWN_PLZ
# from .forms import CaptchaForm

def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    return render(request, 'index.html', context)

# Standorteingabe
def search(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'category': category
    }

    return render(request, 'services/search.html', context)

# Ausgabe der Suchergebnisse einer Branche nach Naehe zu Standort
def category(request, category_id):
    # Daten aufnehmen
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

# Seite eines Service-Providers
def service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    context = {}
    # Kontaktdaten wurden abgerufen, Captcha auslesen
    # context['contact'] = 0
    # if request.method == 'POST':
    #     form = CaptchaForm(request.POST)
    #     if form.is_valid():
    #         context['contact'] = 1
    # else:
    #     form = CaptchaForm()

    # Nutzer ist eingeloggt, hole bestehende Bewertung falls vorhanden
    if request.user.is_authenticated:
        try:
            r = Rating.objects.get(by=request.user,of=service)
            context['rating'] = r
        except:
            pass # FIXME WTF?
        # Bewertung wurde abgegeben/modifiziert
        if 'r' in request.GET:
            try:
                r.stars = int(request.GET['r'])
            except:
                r = Rating(by=request.user,of=service,stars=int(request.GET['r']))
            r.text = request.GET['rt']
            if 6 > int(r.stars) > 0:
                r.save()
            context['rating'] = r

    # Ratings holen
    ratinglist = Rating.objects.filter(of=service).order_by('-at')

    ratings = paginate(ratinglist, 5)

    context['service'] = service
    context['ratings'] = ratings
    # context['form'] = form

    return render(request, 'services/service.html', context)

def manage(request):
    if not request.user.is_authenticated: # FIXME
        return redirect(index)

    return render(request, 'services/manage.html')

def payment(request):
    context = {
        'token': PAYMENT_BACKEND.get_client_token(request.user),
    }

    return render(request, 'services/payment.html', context)

def checkout(request):
    if request.method != 'POST':
        return redirect('/')

    if create_payment(request.user, request.POST.get('payment_method_nonce')):
        return render(request, 'services/payment_complete.html')
    else:
        return render(request, 'services/payment_failed.html')

