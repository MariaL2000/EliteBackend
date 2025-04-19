from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    CommentSerializer, 
    OrderSerializer, 
    ScheduleSerializer,
    SiteConfigurationSerializer
)
from django.core.exceptions import ValidationError
import json
from .models import Comment, Client, Order, SiteConfiguration
#from .forms import OrderForm, CommentForm, ScheduleSelectionForm

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
#from .forms import ScheduleSelectionForm,ClientOrderForm
from django.conf import settings
from urllib.parse import quote
from socket import error as SocketError
import errno
from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes







@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comments_api(request):
    if request.method == "POST":
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'Comment created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Invalid data provided'
        }, status=status.HTTP_400_BAD_REQUEST)

    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': comments.count()
    })



@api_view(['POST'])
@permission_classes([AllowAny])
def contact_api(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        order_details = (
            f"Name: {order.client_name}\n"
            f"Email: {order.email}\n"
            f"Phone: {order.phone}\n"
            f"Address: {order.address}\n"
            f"Project Details: {order.description}\n"
        )
        
        try:
            send_mail(
                subject="New Order Received",
                message=f"New order details:\n\n{order_details}",
                from_email="mariamarreromedrano@gmail.com",
                recipient_list=["mariamarreromedrano@gmail.com"],
                fail_silently=False,
            )
            send_mail(
                subject="Your Order Confirmation",
                message=f"Dear {order.client_name},\n\n{order_details}",
                from_email="mariamarreromedrano@gmail.com",
                recipient_list=[order.email],
                fail_silently=False,
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([AllowAny])
def about_api(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    serializer = SiteConfigurationSerializer(site_config)
    about_data = {
        'company_pictures': [
            getattr(site_config, f'company_picture_{i}').url if getattr(site_config, f'company_picture_{i}') else None
            for i in range(1, 7)
        ],
        'team': {
            'admin': site_config.admin_perfil.url if site_config.admin_perfil else None,
            'admin_2': site_config.admin_2_perfil.url if site_config.admin_2_perfil else None,
            'architect': site_config.architect.url if site_config.architect else None
        },
        'theme': {
            'background_color': site_config.background_color,
            'text_color': site_config.text_color,
            'button_color': site_config.button_color,
            'button_text_color': site_config.button_text_color
        }
    }
    return Response(about_data)










@api_view(['GET'])
@permission_classes([AllowAny])
def gallery_api(request):
    try:
        site_config = SiteConfiguration.objects.order_by("-id").first()
        gallery_data = {
            'bathrooms': [
                {
                    'image': getattr(site_config, f'bathroom_{i}').url if getattr(site_config, f'bathroom_{i}') else None,
                    'price': getattr(site_config, f'price_bathroom_{i}')
                } for i in range(1, 11)
            ],
            'kitchens': [
                {
                    'image': getattr(site_config, f'kitchen_{i}').url if getattr(site_config, f'kitchen_{i}') else None,
                    'price': getattr(site_config, f'price_kitchen_{i}')
                } for i in range(1, 11)
            ],
            'fireplaces': [
                {
                    'image': getattr(site_config, f'fireplace_{i}').url if getattr(site_config, f'fireplace_{i}') else None,
                    'price': getattr(site_config, f'price_fireplace_{i}')
                } for i in range(1, 11)
            ]
        }
        return Response({
            'success': True,
            'data': gallery_data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        



@api_view(['GET'])
@permission_classes([AllowAny])
def bathrooms_api(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    serializer = SiteConfigurationSerializer(site_config)
    bathroom_data = {
        'bathrooms': [
            {
                'image': getattr(site_config, f'bathroom_{i}').url if getattr(site_config, f'bathroom_{i}') else None,
                'price': getattr(site_config, f'price_bathroom_{i}')
            } for i in range(1, 11)
        ]
    }
    return Response(bathroom_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def kitchens_api(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    serializer = SiteConfigurationSerializer(site_config)
    kitchen_data = {
        'kitchens': [
            {
                'image': getattr(site_config, f'kitchen_{i}').url if getattr(site_config, f'kitchen_{i}') else None,
                'price': getattr(site_config, f'price_kitchen_{i}')
            } for i in range(1, 11)
        ]
    }
    return Response(kitchen_data)



@api_view(['GET'])
@permission_classes([AllowAny])
def fireplaces_api(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    serializer = SiteConfigurationSerializer(site_config)
    fireplace_data = {
        'fireplaces': [
            {
                'image': getattr(site_config, f'fireplace_{i}').url if getattr(site_config, f'fireplace_{i}') else None,
                'price': getattr(site_config, f'price_fireplace_{i}')
            } for i in range(1, 11)
        ]
    }
    return Response(fireplace_data)






@api_view(['GET'])
@permission_classes([AllowAny])
def index_api(request):
    site_config = SiteConfiguration.objects.order_by("-id").first()
    serializer = SiteConfigurationSerializer(site_config)
    index_data = {
        'carousel': [
            getattr(site_config, f'image_carrousel_{i}').url if getattr(site_config, f'image_carrousel_{i}') else None
            for i in range(1, 7)
        ],
        'videos': [
            getattr(site_config, f'video_carrousel_{i}').url if getattr(site_config, f'video_carrousel_{i}') else None
            for i in range(1, 4)
        ],
        'countertops': {
            'granite': [
                getattr(site_config, f'granite_countertop_{i}').url if getattr(site_config, f'granite_countertop_{i}') else None
                for i in range(1, 4)
            ],
            'quartz': [
                getattr(site_config, f'quartz_countertop_{i}').url if getattr(site_config, f'quartz_countertop_{i}') else None
                for i in range(1, 4)
            ],
            'quartzite': [
                getattr(site_config, f'quartzite_countertop_{i}').url if getattr(site_config, f'quartzite_countertop_{i}') else None
                for i in range(1, 4)
            ]
        }
    }
    return Response(index_data)









@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def send_email_to_client(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.save()
            order.schedule = schedule
            order.save()
            
            contact_page_url = request.build_absolute_uri(
                reverse("contact_page_api", args=[order.id])
            )
            
            email_data = {
                "subject": f"Order Details - {order.id}",
                "body": f"""
                Dear {order.client_name},
                Your order is scheduled for {schedule.time_slot} on {schedule.date}.
                The approximate price is $XXX.XX.
                You can accept or reject the offer here: {contact_page_url}
                """
            }
            
            return Response({"email_data": email_data, "schedule": serializer.data}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"order_id": order_id})


@api_view(['GET', 'POST'])
def contact_page_api(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        action = request.data.get("action")
        if action == "accept":
            order.status = "accepted"
            order.save()
            subject = f"Order {order.id} Accepted"
            message = f"The customer has accepted the offer for Order ID {order.id}."
        elif action == "reject":
            order.status = "rejected"
            order.save()
            subject = f"Order {order.id} Rejected"
            message = f"The customer has rejected the offer for Order ID {order.id}."
        
        send_mail(
            subject=subject,
            message=message,
            from_email=order.email,
            recipient_list=["mariamarreromedrano@gmail.com"]
        )

        return Response({"status": order.status}, status=status.HTTP_200_OK)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)