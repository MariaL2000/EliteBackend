from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
import json
from .models import Comment, Client, Order, SiteConfiguration
from django.http import HttpResponse, JsonResponse
from .forms import OrderForm, CommentForm, ScheduleSelectionForm
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from django.core.mail import send_mail
from django.urls import reverse
from .forms import ScheduleSelectionForm,ClientOrderForm
from django.conf import settings
from urllib.parse import quote
from socket import error as SocketError
import errno


def comments(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = CommentForm(data)
        if form.is_valid():
            comment = form.save()
            return JsonResponse(
                {
                    "name": comment.name,
                    "opinion": comment.opinion,
                    "rating": comment.rating,
                    "sug": comment.sug,
                },
                status=201,
            )
        return JsonResponse({"errors": form.errors}, status=400)
    else:
        comments = Comment.objects.all()
        return render(request, "orders/reviews.html", {"comments": comments})




def contact(request):
    if request.method == "POST":
        form = ClientOrderForm(request.POST)
        try:
            if form.is_valid():
                order = form.save()
                # Format order details
                order_details = (
                    f"Name: {order.client_name}\n"
                    f"Email: {order.email}\n"
                    f"Phone: {order.phone}\n"
                    f"Address: {order.address}\n"
                    f"Project Details: {order.description}\n"
                )

                # Email to admin
                send_mail(
                    subject="New Order Received",
                    message=f"New order details:\n\n{order_details}",
                    from_email="mariamarreromedrano@gmail.com",
                    recipient_list=["mariamarreromedrano@gmail.com"],
                    fail_silently=False,
                )

                # Email to client
                send_mail(
                    subject="Your Order Confirmation",
                    message=(
                        f"Dear {order.client_name},\n\n"
                        f"Thank you for your order. We have received the following details:\n\n"
                        f"{order_details}\n\n"
                        f"We will contact you shortly.\n\n"
                        f"Best regards,\nTampa Custom Countertops"
                    ),
                    from_email="mariamarreromedrano@gmail.com",
                    recipient_list=[order.email],
                    fail_silently=False,
                )

                return JsonResponse({"success": True}, status=201)
            return JsonResponse({"errors": form.errors}, status=400)
        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=500)
    return render(request, "orders/contact.html", {"form": ClientOrderForm()})





def about(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    return render(request, "orders/about.html", {"site_config": site_config})


def gallery(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    return render(request, "orders/gallery.html", {"site_config": site_config})


def bathrooms(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    return render(request, "orders/bathrooms.html", {"site_config": site_config})


def kitchens(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    return render(request, "orders/kitchens.html", {"site_config": site_config})


def fireplaces(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    return render(request, "orders/fireplaces.html", {"site_config": site_config})


def index(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    return render(request, "orders/index.html", {"site_config": site_config})


def send_email_to_client(request, order_id):
    # Obtener el pedido por ID
    order = get_object_or_404(Order, id=order_id)

    # Si el formulario es enviado
    if request.method == "POST":
        form = ScheduleSelectionForm(request.POST)
        if form.is_valid():
            # Obtener el horario seleccionado
            schedule = form.cleaned_data["schedule"]

            # Asignar el horario al pedido y marcar el horario como no disponible
            order.schedule = schedule
            order.save()

            # Marcar el horario como no disponible
            schedule.is_available = False
            schedule.save()

            # Crear el asunto y cuerpo del correo
            contact_page_url = request.build_absolute_uri(
                reverse("contact_page", args=[order.id])
            )
            subject = f"Order Details - {order.id}"
            body = f"""
            Dear {order.client_name},

            Your order is scheduled for {schedule.time_slot} on {schedule.date}.
            The approximate price is $XXX.XX.

            You can accept or reject the offer by clicking on the link below, else you can send us and email or call us:
            {contact_page_url}

            Thank you for your business!
            Hope to see you soon!
            """

            # Codificar el asunto y el cuerpo para ser utilizados en un enlace mailto
            encoded_subject = quote(subject)
            encoded_body = quote(body)

            # Crear el enlace mailto con los datos precargados
            mailto_link = (
                f"mailto:{order.email}?subject={encoded_subject}&body={encoded_body}"
            )

            # Depuración: mostrar el enlace mailto generado
            print(f"Generated mailto link: {mailto_link}")

            # Redirigir al cliente al enlace de correo para que edite y envíe el mensaje
            return render(
                request,
                "admin/orders/select_schedule.html",
                {"mailto_link": mailto_link, "order": order},
            )

    else:
        form = ScheduleSelectionForm()

    return render(
        request, "admin/orders/select_schedule.html", {"form": form, "order": order}
    )


def contact_page(request, order_id=None):
    if order_id is None:
        return HttpResponse("No order ID provided.", status=400)

    # Obtener el pedido por ID
    order = get_object_or_404(Order, id=order_id)
    user_message = None

    # Si el cliente hace clic en "aceptar" o "rechazar", se procesa
    if request.GET.get("action") == "accept":
        order.status = "accepted"
        order.save()

        # Enviar correo al administrador notificando la aceptación
        subject = f"Order {order.id} Accepted"
        admin_message = f"The customer has accepted the offer for Order ID {order.id}."
        send_mail(
            subject, admin_message, order.email, ["mariamarreromedrano@gmail.com"]
        )

        user_message = "Thank you for accepting the offer!"

    elif request.GET.get("action") == "reject":
        order.status = "rejected"
        order.save()

        # Enviar correo al administrador notificando el rechazo
        subject = f"Order {order.id} Rejected"
        admin_message = f"The customer has rejected the offer for Order ID {order.id}."
        send_mail(
            subject, admin_message, order.email, ["mariamarreromedrano@gmail.com"]
        )

        user_message = "Sorry to hear that the offer was rejected."

    return render(
        request, "orders/contact_page.html", {"order": order, "user_message": user_message}
    )
