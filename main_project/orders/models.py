from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils.safestring import mark_safe

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255) 
    
    def __str__(self):
        return f'{self.name} ({self.email})'

class Comment(models.Model):
    name = models.CharField(max_length=100)
    opinion = models.TextField()
    rating = models.IntegerField()
    sug = models.TextField()

    def __str__(self):
        return self.name

    def clean(self):
        """Método de validación para rating."""
        if not (0 <= self.rating <= 5):
            raise ValidationError("Rating must be between 0 and 5.")

    def save(self, *args, **kwargs):
        self.clean()  # Aseguramos que la validación se ejecute al guardar
        super().save(*args, **kwargs)





from django.db import models
from django.core.exceptions import ValidationError

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client_name = models.CharField(max_length=255)
    description = models.TextField(help_text='Describe your needs')
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    schedule = models.ForeignKey('Schedule', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Order #{self.id} - {self.client_name}'

    def safe_description(self):
        return mark_safe(self.description)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def save(self, *args, **kwargs):
        # Si la orden tiene un schedule asignado, marcamos el schedule como no disponible
        if self.schedule and self.schedule.is_available:
            self.schedule.is_available = False
            self.schedule.save()
        super().save(*args, **kwargs)



class Schedule(models.Model):
    time_slot = models.CharField(max_length=50)
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} - {self.time_slot}"

    def clean(self):
        if Schedule.objects.filter(date=self.date, time_slot=self.time_slot).exists():
            raise ValidationError("This time slot is already booked.")



from django.db import models
from django.core.exceptions import ValidationError

class SiteConfiguration(models.Model):
    background_color = models.CharField(max_length=7, default="#ffffff", help_text="Background color in hex format")
    text_color = models.CharField(max_length=7, default="#000000", help_text="Text color in hex format")
    button_color = models.CharField(max_length=7, default="#007bff", help_text="Button color in hex format")
    button_text_color = models.CharField(max_length=7, default="#ffffff", help_text="Button text color in hex format")
    

    #las 3 primeras son para gallery
    bathroom_1 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_2 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_3 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_4 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_4 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_5 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_6 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_6 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_7 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_7 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_8 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_8 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_9 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_9 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bathroom_10 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_bathroom_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  
    

    kitchen_1 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_2 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_3 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_4 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_4 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_5 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_6 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_6 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_7 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_7 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_8 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_8 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_9 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_9 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kitchen_10 = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_kitchen_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
   
   
    fireplace_1= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_2= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_3= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_4= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_4 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_5= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_6= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_6 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_7= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_7 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_8= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_8 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_9= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_9 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fireplace_10= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    price_fireplace_10 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


#para el index
    image_carrousel_1= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    image_carrousel_2= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    image_carrousel_3= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    image_carrousel_4= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    image_carrousel_5= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    image_carrousel_6= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    granite_countertop_1= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    granite_countertop_2= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    granite_countertop_3= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    quartz_countertop_1= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    quartz_countertop_2= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    quartz_countertop_3= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    quartzite_countertop_1= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    quartzite_countertop_2= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    quartzite_countertop_3= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    video_carrousel_1 = models.FileField(upload_to='videos/', blank=True, null=True)
    video_carrousel_2 = models.FileField(upload_to='videos/', blank=True, null=True)
    video_carrousel_3 = models.FileField(upload_to='videos/', blank=True, null=True)




#para el about
    admin_perfil= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    admin_2_perfil= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    architect= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    company_picture_1= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    company_picture_2= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    company_picture_3= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    company_picture_4= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    company_picture_5= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    company_picture_6= models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    



    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configurations"

    def save(self, *args, **kwargs):
        if not self.pk and SiteConfiguration.objects.exists():
            # Si ya existe una instancia, actualiza la existente
            existing_config = SiteConfiguration.objects.first()
            self.pk = existing_config.pk
        super(SiteConfiguration, self).save(*args, **kwargs)