import random

from django.http import HttpRequest, Http404
from django.shortcuts import render
import tours.data


# Create your views here.
def main_view(request: HttpRequest):
    output_tours_ids = random.sample(range(1, len(tours.data.tours) + 1), 6)
    output_tours = {}

    for output_tour_id in output_tours_ids:
        output_tour = dict(tours.data.tours[output_tour_id])
        output_tours.update({
            output_tour_id:
                {
                    'title': output_tour['title'],
                    'description': output_tour['description'],
                    'picture': output_tour['picture']
                }
        })
    return render(request, 'tours/index.html', context={
        'tours': output_tours,
        'departures': tours.data.departures
    })


def departure_view(request: HttpRequest, departure: str):
    try:
        output_departure = tours.data.departures[departure]
    except KeyError:
        raise Http404

    output_tours = {}
    nights = [-1, -1]               # хранит минимальное и максимальное значение
    prices = list(nights)           # хранит минимальное и максимальное значение
    for tour_id, tour in tours.data.tours.items():
        if tour['departure'] == departure:
            output_tours.update({
                tour_id:
                    {
                        'title': tour['title'],
                        'description': tour['description'],
                        'picture': tour['picture']
                    }
            })
            if tour['nights'] > nights[1] == -1:
                nights[1] = tour['nights']
                if nights[0] == -1:
                    nights[0] = nights[1]
            if tour['nights'] < nights[0]:
                nights[0] = tour['nights']

            if tour['price'] > prices[1]:
                prices[1] = tour['price']
                if prices[0] == -1:
                    prices[0] = prices[1]
            if tour['price'] < prices[0]:
                prices[0] = tour['price']

    return render(request, 'tours/departure.html', context={
        'departures': tours.data.departures,
        'active_departure': output_departure,
        'quantity': len(output_tours),
        'prices': prices,
        'nights': nights,
        'tours': output_tours
    })


def tour_view(request: HttpRequest, id: int):
    output_tour = dict(tours.data.tours[id])
    output_tour['departure'] = tours.data.departures[output_tour['departure']]
    return render(request, 'tours/tour.html', context={
        'departures': tours.data.departures,
        'tour': output_tour
    })
