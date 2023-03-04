from pathlib import Path
import requests
from urllib.parse import unquote, urlparse

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place, Image


class Command(BaseCommand):
    help = 'Команда для заполнения сайта данными из выбранного файла .json'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, nargs='+', help='Адрес файла .json.')

    def save_images(self, place, img_urls):
        for order, img_url in enumerate(img_urls):
            filename = unquote(Path(urlparse(img_url).path).name)
            try:
                image_response = requests.get(img_url)
                image_response.raise_for_status()
            except requests.exceptions.HTTPError:
                self.stderr.write(self.style.ERROR(
                    f'Картинка по адресу {img_url} не найдена'))

            image_content = ContentFile(image_response.content, name=filename)
            Image(number=order, place=place, image=image_content).save()

    def handle(self, *args, **options):
        for place_url in options['json_url']:
            try:
                place_response = requests.get(place_url)
                place_response.raise_for_status()
                place = place_response.json()
            except requests.exceptions.HTTPError:
                self.stderr.write(self.style.ERROR(
                    f"Описание локации по адресу {options['json_url']} не найдено"))
                continue

            try:
                place_created, created = Place.objects.get_or_create(
                    title=place['title'],
                    lng=place['coordinates']['lng'],
                    lat=place['coordinates']['lat'],
                    defaults={
                        'description_short': place.get('description_short', ''),
                        'description_long': place.get('description_long', ''),
                    }
                )
            except KeyError as exception:
                self.stderr.write(self.style.ERROR(
                    f'Недоступно поле "{exception.args[0]}" '))
                continue

            if created:
                image_urls = place.get('imgs', [])
                self.save_images(place_created, image_urls)
