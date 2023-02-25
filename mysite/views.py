from django.http import HttpResponse
from django.shortcuts import render
from places.models import Place, Image

def show_main(request):
    places = Place.objects.all()
    places_description = []
    for place in places:
        description = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.lng, place.lat]
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": "https://raw.githubusercontent.com/devmanorg/where-to-go-frontend/master/places/roofs24.json"
                    }
                }
            ]
        }
        places_description.append(description)

    return render(request, 'index.html', {'places_geojson': places_description})