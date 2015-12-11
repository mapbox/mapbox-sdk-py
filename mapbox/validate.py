
def lat(val):
    if val is not None and (val < -90 or val > 90):
        raise ValueError("Latitude must be between -90 and 90")
    return val

def lon(val):
    if val is not None and (val < -180 or val > 180):
        raise ValueError("Longitude must be between -180 and 180")
    return val
