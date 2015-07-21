import requests


def surface(mapid, points, access_token, **kwargs):
    queryParams = {
        'access_token': access_token,
        'points': ';'.join([
            ','.join([
                str(ll) for ll in pt
            ]) for pt in points
        ])
    }

    if not 'layer' in kwargs:
        raise ValueError('<layer> must be provided')
    else:
        queryParams['layer'] = kwargs['layer']

    if 'fields' in kwargs:
        if type(kwargs['fields']) != type([]):
            raise ValueError('<fields> must be a list of values')
        else:
            queryParams['fields'] = ','.join([
                str(f) for f in kwargs['fields']
                ])

    if 'zoom' in kwargs:
        if type(kwargs['zoom']) != int:
            raise ValueError('zoom must be an integer')
        else:
            queryParams['zoom'] = int(kwargs['zoom'])

    queryUrl = 'https://api.mapbox.com/v4/surface/%s.json' % (mapid,)

    surface_request = requests.get(queryUrl, params=queryParams)
    surface_request.raise_for_status()

    return surface_request.json()

if __name__ == '__main__':
    surface()