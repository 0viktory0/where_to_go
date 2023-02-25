from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200, db_index=True)
    description_short = models.TextField('Короткое описание', blank=True)
    description_long = models.TextField('Длинное описание', blank=True)
    lng = models.FloatField('Широта')
    lat = models.FloatField('Долгота')


    def __str__(self):
        return f'{self.title}'

    class Meta(object):
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Image(models.Model):
    image = models.ImageField('Картинка')
    number = models.PositiveIntegerField('Позиция', default=0, blank=True, null=False,)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')



    def __str__(self):
        return f'{self.number}. {self.place.title}'

    class Meta(object):
        ordering = ['number']
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'