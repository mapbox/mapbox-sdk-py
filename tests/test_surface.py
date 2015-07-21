import mapbox
import click
import pytest
import requests

def test_mapbox():
    with mapbox.Mapbox('abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123') as mbx:
        assert mbx.exists() == 'Mapbox exists with access token abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123'


def test_surface_bad():
    """Test for raising bad errors"""
    query_points = [
            [-122.46477127075194, 37.77641361883315],
            [-122.43558883666992, 37.76447260365713],
            [-122.40606307983398, 37.75117238560617],
            [-122.43009567260741, 37.745471560181194], 
            [-122.45859146118164, 37.73651223296987],
            [-122.48674392700195, 37.73406859189756]
        ]
    
    with mapbox.Mapbox('abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123') as mbx:
        with pytest.raises(requests.exceptions.HTTPError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                query_points,
                layer='contour',
                fields=['ele'])

        with pytest.raises(TypeError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                query_points,
                layer=100,
                fields=['ele'])

        with pytest.raises(TypeError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                query_points,
                layer='contour',
                fields='ele')

        with pytest.raises(TypeError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                query_points,
                layer='contour',
                fields=['ele'],
                zoom='one_bad_dude')

        with pytest.raises(ValueError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                query_points,
                fields=['ele'])

        with pytest.raises(ValueError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                query_points,
                layer='contour')

        with pytest.raises(TypeError):
            surface_response = mbx.surface('mapbox.mapbox-terrain-v2',
                [1,2],
                layer='contour',
                fields=['ele'])