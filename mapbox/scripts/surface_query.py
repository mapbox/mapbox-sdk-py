import requests
import api_utils


def surface(mapid, points, access_token, **kwargs):
    queryParams = {
        'access_token': access_token,
        'points': api_utils.lat_lng_formatter(points)
    }

    params = {
        'layer': {
            'required': True,
            'type': str
        },
        'fields': {
            'required': True,
            'type': list
        },
        'zoom': {
            'type': int
        }
    }
    queryParams = api_utils.validator(params, kwargs, queryParams)

    queryUrl = 'https://api.mapbox.com/v4/surface/%s.json' % (mapid,)

    surface_request = requests.get(queryUrl, params=queryParams)
    surface_request.raise_for_status()

    return surface_request.json()

if __name__ == '__main__':
    surface()