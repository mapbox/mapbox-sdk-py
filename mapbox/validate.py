
def lat(val):
    if val is not None and (val < -90 or val > 90):
        raise ValueError("Latitude must be between -90 and 90")
    return val

def lon(val):
    if val is not None and (val < -180 or val > 180):
        raise ValueError("Longitude must be between -180 and 180")
    return val

def size(val):
    if not (1 < val[0] < 1280) and not (1 < val[1] < 1280):
        raise ValueError("Image height and width must be between 1 and 1280")
    return val
