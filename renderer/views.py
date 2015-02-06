from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import sqrt

from notdienste.settings import SUPPORT_EMAIL
from services.models import *
from payments.backends import BraintreeBackend
# from .forms import CaptchaForm

PAYMENT_BACKEND = BraintreeBackend()

def index(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'index.html', context)

# Standorteingabe
def search(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'category': category}
    return render(request, 'services/search.html', context)

# Ausgabe der Suchergebnisse einer Branche nach Naehe zu Standort
def category(request, category_id):
    # Daten aufnehmen
    category = get_object_or_404(Category, pk=category_id)
    try:
        plz = Location.objects.get(plz=request.GET['plz'])
    except:
        error = """Dies scheint keine uns bekannte Postleitzahl zu sein. Im \
        Falle eines Fehlers kontaktieren sie uns bitte unter %s.""" % \
        SUPPORT_EMAIL
        return render(request, 'error.html', {'error': error})
    services = Service.objects.filter(category=category)
    # GPS-Koordinaten aus DB lesen und zuweisen, Entfernungsberechnung
    distances = {}
    for service in services:
        if service.lon <= plz.lon:
            dlon = plz.lon - service.lon
        else:
            dlon = service.lon - plz.lon
        if service.lat <= plz.lat:
            dlat = plz.lat - service.lat
        else:
            dlat = service.lat - plz.lat
        kdlon = dlon * 71.5
        kdlat = dlat * 111.3
        distances[service] = round(sqrt(kdlon * kdlon + kdlat * kdlat), 2)
    slist = []
    for service in distances:
        slist += [(distances[service], service)]
    # Sortierung nach Entfernung
    slist.sort()
    # Paginator
    paginator = Paginator(slist, 10)
    page = request.GET.get('p')
    try:
        servicelist = paginator.page(page)
    except PageNotAnInteger:
        servicelist = paginator.page(1)
    except EmptyPage:
        servicelist = paginator.page(paginator.num_pages)
    # Rendering
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
            pass
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
    paginator = Paginator(ratinglist, 5)
    page = request.GET.get('p')
    try:
        ratings = paginator.page(page)
    except PageNotAnInteger:
        ratings = paginator.page(1)
    except EmptyPage:
        ratings = paginator.page(paginator.num_pages)
    context['service'] = service
    context['ratings'] = ratings
    # context['form'] = form
    return render(request, 'services/service.html', context)

def payment(request):
    context = {
        'token': PAYMENT_BACKEND.get_client_token(request.user),
    }
    return render(request, 'services/payment.html', context)

def checkout(request):
    if request.method != 'POST':
        return redirect('/')

    pm = PAYMENT_BACKEND.create_payment_method(request.user,
            request.POST.get('payment_method_nonce'))
    tr = PAYMENT_BACKEND.create_transaction('10.00', pm.payment_method.token)
    result = PAYMENT_BACKEND.submit_settlement(tr.transaction.id)
    if result.is_success:
        return render(request, 'services/payment_complete.html')
    else:
        return render(request, 'services/payment_failed.html')

