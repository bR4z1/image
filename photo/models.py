from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User


class AlbumPhoto(models.Model):
    user = models.ForeignKey(User, default=1)
    photo_title = models.CharField(max_length=250)
    genre = models.CharField(max_length=100)
    photo_logo = models.ImageField(
        null=True, 
        blank=True,
        height_field = "height_field",
        width_field = "width_field",
        )
    
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    
    
    def get_absolute_url(self):
        return reverse('photo:detail', kwargs={"id": self.id})

    def __str__(self):
        return self.photo_title + ' - ' + self.genre
    

