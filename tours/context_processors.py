import tours.data


def default_data(request):
    return {
        'title': tours.data.title,
        'departures': tours.data.departures
    }
