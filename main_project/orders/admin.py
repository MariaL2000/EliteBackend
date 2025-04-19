from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from .serializers import SiteConfigurationSerializer, OrderSerializer, CommentSerializer, ScheduleSerializer
from .models import Order, Comment, Schedule, SiteConfiguration
from .forms import SiteConfigurationForm, OrderForm
from reportlab.pdfgen import canvas

from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    serializer_class = ScheduleSerializer
    list_display = ('time_slot', 'date', 'is_available')
    search_fields = ('time_slot', 'date')
    list_filter = ('is_available', 'date')
    actions = ['mark_as_available', 'mark_as_unavailable']

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
    mark_as_available.short_description = "Mark selected schedules as Available"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    mark_as_unavailable.short_description = "Mark selected schedules as Unavailable"



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    serializer_class = OrderSerializer
    list_display = ("id", "get_client_name", "description", "phone", "email", 
                   "status", "address", "date", "schedule", "send_email_link")
    list_filter = ("status",)
    actions = ["generate_pdf", "mark_as_pending", "mark_as_in_progress", 
              "mark_as_completed", "mark_as_cancelled"]
    ordering = ["date", "schedule"]



    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def has_change_permission(self, request, obj=None):
        return False  # Evita que se editen horarios desde el formulario de Orders

    def has_delete_permission(self, request, obj=None):
        return False  # Evita que se eliminen horarios desde el formulario de Orders
    
    def has_add_permission(self, request):
        return True  # Asegúrate de que esto retorne True si quieres permitir agregar órdenes


    def get_client_name(self, obj):
        return obj.client_name

    get_client_name.short_description = "Client"

    def send_email_link(self, obj):
        # Generar enlace para enviar el correo
        url = reverse("send_email_to_client", args=[obj.id])
        return format_html('<a href="{}">Send Email</a>', url)

    send_email_link.short_description = "Send Email"

    # Acciones adicionales como generar PDF, marcar estado, etc.
    def generate_pdf(self, request, queryset):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="orders.pdf"'

        pdf = canvas.Canvas(response)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 800, "Lista de Pedidos")

        y = 780
        for order in queryset:
            pdf.drawString(
                100,
                y,
                f"ID: {order.id} | Cliente: {order.client_name} | Descripción: {order.description} | Teléfono: {order.phone} | Email: {order.email} | Estado: {order.status} | Fecha: {order.date}",
            )
            y -= 20

        pdf.showPage()
        pdf.save()
        return response

    def mark_as_pending(self, request, queryset):
        queryset.update(status="pending")

    mark_as_pending.short_description = "Mark selected orders as Pending"

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status="in_progress")

    mark_as_in_progress.short_description = "Mark selected orders as In Progress"

    def mark_as_completed(self, request, queryset):
        queryset.update(status="completed")

    mark_as_completed.short_description = "Mark selected orders as Completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")

    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    serializer_class = CommentSerializer
    list_display = ("name", "opinion", "rating", "sug")
    search_fields = ("name", "opinion")
    list_filter = ("rating",)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    serializer_class = SiteConfigurationSerializer
    list_display = ("background_color", "text_color", "button_color", "button_text_color")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "background_color",
                    "text_color",
                    "button_color",
                    "button_text_color",
                )
            },
        ),
        (
            "Bathrooms",
            {
                "fields": (
                    "bathroom_1",
                    "price_bathroom_1",
                    "bathroom_2",
                    "price_bathroom_2",
                    "bathroom_3",
                    "price_bathroom_3",
                    "bathroom_4",
                    "price_bathroom_4",
                    "bathroom_5",
                    "price_bathroom_5",
                    "bathroom_6",
                    "price_bathroom_6",
                    "bathroom_7",
                    "price_bathroom_7",
                    "bathroom_8",
                    "price_bathroom_8",
                    "bathroom_9",
                    "price_bathroom_9",
                    "bathroom_10",
                    "price_bathroom_10",
                )
            },
        ),
        (
            "Kitchens",
            {
                "fields": (
                    "kitchen_1",
                    "price_kitchen_1",
                    "kitchen_2",
                    "price_kitchen_2",
                    "kitchen_3",
                    "price_kitchen_3",
                    "kitchen_4",
                    "price_kitchen_4",
                    "kitchen_5",
                    "price_kitchen_5",
                    "kitchen_6",
                    "price_kitchen_6",
                    "kitchen_7",
                    "price_kitchen_7",
                    "kitchen_8",
                    "price_kitchen_8",
                    "kitchen_9",
                    "price_kitchen_9",
                    "kitchen_10",
                    "price_kitchen_10",
                )
            },
        ),
        (
            "Fireplaces",
            {
                "fields": (
                    "fireplace_1",
                    "price_fireplace_1",
                    "fireplace_2",
                    "price_fireplace_2",
                    "fireplace_3",
                    "price_fireplace_3",
                    "fireplace_4",
                    "price_fireplace_4",
                    "fireplace_5",
                    "price_fireplace_5",
                    "fireplace_6",
                    "price_fireplace_6",
                    "fireplace_7",
                    "price_fireplace_7",
                    "fireplace_8",
                    "price_fireplace_8",
                    "fireplace_9",
                    "price_fireplace_9",
                    "fireplace_10",
                    "price_fireplace_10",
                )
            },
        ),
        (
            "Initial Page",
            {
                "fields": (
                    "image_carrousel_1",
                    "image_carrousel_2",
                    "image_carrousel_3",
                    "image_carrousel_4",
                    "image_carrousel_5",
                    "image_carrousel_6",
                    "granite_countertop_1",
                    "granite_countertop_2",
                    "granite_countertop_3",
                    "quartz_countertop_1",
                    "quartz_countertop_2",
                    "quartz_countertop_3",
                    "quartzite_countertop_1",
                    "quartzite_countertop_2",
                    "quartzite_countertop_3",
                    "video_carrousel_1",
                    "video_carrousel_2",
                    "video_carrousel_3",
                )
            },
        ),
        (
            "About us page",
            {
                "fields": (
                    "company_picture_1",
                    "company_picture_2",
                    "company_picture_3",
                    "company_picture_4",
                    "company_picture_5",
                    "company_picture_6",
                    "admin_perfil",
                    "admin_2_perfil",
                    "architect",
                )
            },
        ),
    )
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


    class Media:
        js = ("js/jscolor.js",)

