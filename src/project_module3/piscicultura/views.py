from django.shortcuts import render
from .forms import PozoForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "piscicultura/index.html", {})

@login_required
def registrar_pozo(request):
    pozo = PozoForm()
    if request.POST:
        pozo = PozoForm(request.POST)
        print(pozo.is_valid())
        if pozo.is_valid():
            pozo.save()
            return render(request, "piscicultura/index.html", {"registro": "registro exitoso del pozo"})
    else:
        respuesta = {"pozo": pozo}
    return render(request,"piscicultura/registrar_pozo.html",respuesta)