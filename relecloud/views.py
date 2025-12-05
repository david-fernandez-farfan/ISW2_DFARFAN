from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Destination, Cruise, Review, InfoRequest, Purchase
from .forms import InfoRequestForm, ReviewForm 
from django.contrib import messages


# ============================
# VISTAS BÁSICAS
# ============================
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    destinations_qs = Destination.objects.annotate(
        num_reviews=Count("reviews"),
        avg_rating=Avg("reviews__rating"),
    ).order_by("-num_reviews", "-avg_rating", "name")

    return render(request, "destinations.html", {
        "destinations": destinations_qs
    })


# ============================
# INFO REQUEST (EMAILS)
# ============================
def info_request_view(request):
    if request.method == "POST":
        form = InfoRequestForm(request.POST)
        if form.is_valid():
            info_obj = form.save()

            # 1️⃣ Correo al cliente
            send_mail(
                subject=f"ReleCloud – Solicitud #{info_obj.id}",
                message=(
                    "Hola,\n\n"
                    "Hemos recibido tu solicitud de información sobre nuestros cruceros.\n"
                    "Nuestro equipo contactará contigo pronto.\n\n"
                    "Gracias por confiar en ReleCloud.\n"
                ),
                from_email=f"ReleCloud <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[info_obj.email],
                fail_silently=False,
            )

            # 2️⃣ Correo al administrador
            send_mail(
                subject=f"Nueva solicitud #{info_obj.id}",
                message=(
                    f"Nombre: {info_obj.name}\n"
                    f"Email: {info_obj.email}\n"
                    f"Cruise: {info_obj.cruise}\n"
                    f"Notas: {info_obj.notes}\n"
                ),
                from_email=f"ReleCloud <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[settings.SUPPORT_EMAIL],
                fail_silently=False,
            )

            return redirect("info_request_success")

    else:
        form = InfoRequestForm()

    return render(request, "info_request.html", {"form": form})

# ============================
# DESTINATION DETAIL
# ============================
class DestinationDetailView(generic.DetailView):
    model = Destination
    template_name = 'destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.object  # 👈 destino actual (el de /destination/1/)
        
        # Lista de reviews para este destino
        context["reviews"] = Review.objects.filter(destination=destination)

        # Puede valorar o no (PT3)
        context["can_review"] = user_has_purchased_destination(self.request.user, destination)

        return context
    
# ============================
# CRUISE DETAIL
# ============================
class CruiseDetailView(generic.DetailView):
    model = Cruise
    template_name = 'cruise_detail.html'
    context_object_name = 'cruise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(cruise=self.object)
        return context


# ============================
# INFO REQUEST (CLASS)
# ============================
class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request.html'
    model = Cruise
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = (
        'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'
    )

def success_view(request):
    return render(request, "success.html")

# ============================
# REVIEW CREATE
# ============================
class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ["rating", "comment"]
    template_name = "review_form.html"

    def form_valid(self, form):
        # Identificar si el review es para DESTINO o CRUCERO
        destination_id = self.kwargs.get("destination_id")
        cruise_id = self.kwargs.get("cruise_id")

        if destination_id:
            form.instance.destination = get_object_or_404(Destination, pk=destination_id)
        if cruise_id:
            form.instance.cruise = get_object_or_404(Cruise, pk=cruise_id)

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige al detalle correspondiente
        if self.object.destination:
            return reverse_lazy("destination_detail", args=[self.object.destination.id])
        else:
            return reverse_lazy("cruise_detail", args=[self.object.cruise.id])
        
        
    # def dispatch(self, request, *args, **kwargs):
    #     destination_id = kwargs.get("destination_id")
    #     cruise_id = kwargs.get("cruise_id")

    #     # Caso: review para DESTINATION
    #     if destination_id:
    #         destination = get_object_or_404(Destination, pk=destination_id)
    #         if not user_has_purchased_destination(request.user, destination):
    #             messages.error(request, "No puedes valorar este destino porque no has comprado ningún crucero asociado.")
    #             return redirect("destination_detail", pk=destination.id)

    #     # (Si tuvieras lógica similar para cruceros, la pondríamos aquí)

    #     return super().dispatch(request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
            destination_id = kwargs.get("destination_id")
            cruise_id = kwargs.get("cruise_id")

    # Caso: review para DESTINATION
            if destination_id:
                destination = get_object_or_404(Destination, pk=destination_id)
                if not user_has_purchased_destination(request.user, destination):
                    messages.error(request, "No puedes valorar este destino porque no has comprado ningún crucero asociado.")
                    return redirect("destination_detail", pk=destination.id)

            # ✔ NUEVO: Caso REVIEW PARA CRUISE
            if cruise_id:
                if not request.user.is_authenticated:
                    messages.error(request, "Debes iniciar sesión para valorar un crucero.")
                    return redirect("login")

                cruise = get_object_or_404(Cruise, pk=cruise_id)

                if not Purchase.objects.filter(user=request.user, cruise=cruise).exists():
                    messages.error(request, "No puedes valorar un crucero que no has comprado.")
                    return redirect("cruise_detail", pk=cruise.id)


            return super().dispatch(request, *args, **kwargs)

    
    def form_valid(self, form):
        # Identificar si el review es para DESTINO o CRUCERO
        destination_id = self.kwargs.get("destination_id")
        cruise_id = self.kwargs.get("cruise_id")

        if destination_id:
            form.instance.destination = get_object_or_404(Destination, pk=destination_id)
        if cruise_id:
            form.instance.cruise = get_object_or_404(Cruise, pk=cruise_id)

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige al detalle correspondiente
        if self.object.destination:
            return reverse_lazy("destination_detail", args=[self.object.destination.id])
        else:
            return reverse_lazy("cruise_detail", args=[self.object.cruise.id])
        
# ============================
# HELPERS PT3
# ============================

def user_has_purchased_destination(user, destination: Destination) -> bool:

    if not user.is_authenticated:
        return False

    # ⚠️ De momento ponemos True para poder probar la PT3.
    # Cuando tengas el modelo de compra, sustituye esta línea por la consulta real.
    return True


def user_has_purchased_destination(user, destination: Destination) -> bool:
    """
    Devuelve True si el usuario ha comprado un crucero
    que tenga este destino asociado.
    """
    if not user.is_authenticated:
        return False

    return Purchase.objects.filter(
        user=user,
        cruise__destinations=destination
    ).exists()