import mapbox
import click

def test_mapbox():
    with mapbox.Mapbox('abcdefg') as mbx:
        assert mbx.exists() == "Mapbox exits with access token abcdefg"
