from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch  import receiver
from django.http import Http404
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    bio = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()  

    class Meta:
        db_table = 'profile'

    @receiver(post_save, sender=User)
    def update_create_profile(sender,instance,created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


    def save_profile(self):
        self.save()


class Products(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image')
    quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
  

    def __str__(self):
        return self.item_name

    def save_product(self):
        self.save()

    def delete_product(self):
        self.delete()

    def search_products(cls,search_term):
        return cls.objects.filter(Q(item_name__icontains=search_term)|Q(description__icontains=search_term)|Q(brand__icontains=search_term))
