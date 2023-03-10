from django.shortcuts import render, get_object_or_404
from places.models import Place
from django.http.response import JsonResponse
from django.urls import reverse


def show_main(request):
    places = Place.objects.all()
    place_descriptions = []
    for place in places:
        description = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [place.lng, place.lat],
                    },
                    'properties': {
                        'title': place.title,
                        'placeId': place.id,
                        'detailsUrl': reverse(get_place, args=[place.id]),
                    },
                },
            ],
        }
        place_descriptions.append(description)
    return render(request, 'index.html', {'places_geojson': place_descriptions})


def get_place(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    content = {
        'title': place.title,
        'imgs': [image.image.url for image in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lng,
        },
    }
    return JsonResponse(
        content,
        json_dumps_params={'ensure_ascii': False, 'indent': 2},
    )
