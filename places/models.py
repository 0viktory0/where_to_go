from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Короткое описание', blank=True)
    description_long = HTMLField('Полное описание', blank=True)
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    class Meta(object):
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField('Картинка')
    number = models.PositiveIntegerField('Позиция', default=0, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')

    class Meta(object):
        ordering = ['number']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return f'{self.number}. {self.place.title}'
