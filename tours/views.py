import random

from django.http import HttpRequest, Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
import tours.data


def error404_view(request: HttpRequest, exception=None):
    return HttpResponseNotFound('<h1>Error 404</h1><p>Page Not Found</p>')


def error500_view(request: HttpRequest, exception=None):
    return HttpResponseServerError("<h1>Error 500</h1><p>That's a crap</p>")


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

    return render(
        request,
        'tours/index.html',
        context={
            'subtitle': tours.data.subtitle,
            'head_title': tours.data.head_title,
            'description': tours.data.description,
            'tours': output_tours,
        }
    )


def departure_view(request: HttpRequest, departure: str):
    try:
        output_departure = tours.data.departures[departure]
    except KeyError:
        raise Http404

    output_tours = {}
    min_max_nights = [-1, -1]               # хранит минимальное и максимальное значение
    min_max_prices = [-1, -1]               # хранит минимальное и максимальное значение

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

            # находим минимальное и максимальное значение ночей и цен
            if tour['nights'] > min_max_nights[1] == -1:
                min_max_nights[1] = tour['nights']
                if min_max_nights[0] == -1:
                    min_max_nights[0] = min_max_nights[1]
            if tour['nights'] < min_max_nights[0]:
                min_max_nights[0] = tour['nights']

            if tour['price'] > min_max_prices[1]:
                min_max_prices[1] = tour['price']
                if min_max_prices[0] == -1:
                    min_max_prices[0] = min_max_prices[1]
            if tour['price'] < min_max_prices[0]:
                min_max_prices[0] = tour['price']

    return render(
        request,
        'tours/departure.html',
        context={
            'active_departure': output_departure,
            'quantity': len(output_tours),
            'prices': min_max_prices,
            'nights': min_max_nights,
            'tours': output_tours
        }
    )


def tour_view(request: HttpRequest, tour_id: int):
    try:
        output_tour = dict(tours.data.tours[tour_id])
    except KeyError:
        raise Http404

    output_tour['departure'] = tours.data.departures[output_tour['departure']]

    return render(
        request,
        'tours/tour.html',
        context={
            'tour': output_tour
        }
    )
