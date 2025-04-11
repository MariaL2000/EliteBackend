from django.test import TestCase
# tests.py
import pytest
from django.core import mail
from django.urls import reverse
from django.test import Client
from .models import Client, Service, Order
from django.conf import settings

@pytest.mark.django_db
def test_create_order_sends_emails():
    # Crear cliente y servicio
    client = Client.objects.create(name="Juan Pérez", email="juan@example.com", address="Calle Ficticia 123", phone="123456789")
    service = Service.objects.create(name="Remodelación de Cocina", description="Reparación de cocina", price=200)

    # Crear pedido
    order = Order.objects.create(
        client=client,
        service=service,
        description="Instalación de nuevos electrodomésticos",
        material="Cocina acero inoxidable",
        price=200
    )

    # Verificar que se haya enviado el correo al admin
    assert len(mail.outbox) == 2  # Deberían enviarse dos correos: uno al admin y otro al cliente

    # Verificar el correo al administrador
    admin_email = mail.outbox[0]
    assert admin_email.subject == 'Nueva Orden Recibida'
    assert admin_email.to == ['admin@example.com']
    assert 'Se ha recibido una nueva orden' in admin_email.body

    # Verificar el correo al cliente
    client_email = mail.outbox[1]
    assert client_email.subject == 'Confirmación de Pedido'
    assert client_email.to == ['juan@example.com']
    assert 'Gracias por realizar un pedido' in client_email.body

@pytest.mark.django_db
def test_order_form_validation():
    # Simula un cliente y un servicio
    client = Client.objects.create(name="Maria Gómez", email="maria@example.com", address="Av. Siempre Viva 456", phone="987654321")
    service = Service.objects.create(name="Pintura de paredes", description="Pintura interior", price=150)

    # Verificar si el formulario de pedido es válido
    order_data = {
        'client': client,
        'service': service,
        'description': "Pintura en sala",
        'material': "Pintura blanca",
        'price': 150
    }

    order = Order(**order_data)
    order.full_clean()  # Esto valida el formulario (automáticamente ejecuta las validaciones)
    order.save()

    # Verificar que el pedido fue guardado
    assert Order.objects.count() == 1
    assert order.client.name == "Maria Gómez"
    assert order.price == 150
