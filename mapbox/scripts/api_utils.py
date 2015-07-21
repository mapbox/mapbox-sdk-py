def validator(params, kwargs, queryParams={}):
    for k in params.keys():
        if k in kwargs:
            if 'type' in params[k] and type(kwargs[k]) != params[k]['type']:
                raise ValueError("%s must be a %s" % (k, params[k]['type']))
            else:
                queryParams[k] = kwargs[k]
        elif 'required' in params[k]:
            raise ValueError("%s must be provided" % (k,))
    return queryParams

def lat_lng_formatter(points):
    return ';'.join([
        ','.join([
            str(ll) for ll in pt
        ]) for pt in points
    ])

if __name__ == '__main__':
    validator()
    lat_lng_formatter()