def validator(params, kwargs, queryParams={}):
    for k in params.keys():
        if k in kwargs:
            if 'type' in params[k] and type(kwargs[k]) != params[k]['type']:
                raise TypeError("%s must be a %s" % (k, params[k]['type']))
            else:
                queryParams[k] = kwargs[k]
        elif 'required' in params[k]:
            raise ValueError("%s must be provided" % (k,))
    return queryParams

def lat_lng_formatter(points):
    try:
        return ';'.join([
            ','.join([
                str(ll) for ll in pt
            ]) for pt in points
        ])
    except:
        raise TypeError("points improperly formatted")

if __name__ == '__main__':
    validator()
    lat_lng_formatter()