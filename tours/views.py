from django.http import HttpRequest, Http404
from django.shortcuts import render

# ограничиваем список возможных направлений
departures = {
    'mos': 'Москвы',
    'spb': 'Петербурга',
    'nvs': 'Новосибирска',
    'ekb': 'Екатеринбурга',
    'kzn': 'Казани'
}


# Create your views here.
def main_view(request: HttpRequest):
    return render(request, 'tours/index.html')


def departure_view(request: HttpRequest, departure: str):
    try:
        output_departure = departures[departure]
    except KeyError:
        raise Http404

    return render(request, 'tours/departure.html', context={
        'departure': output_departure
    })


def tour_view(request: HttpRequest, id: int):
    return render(request, 'tours/tour.html', context={
        'id': id
    })
