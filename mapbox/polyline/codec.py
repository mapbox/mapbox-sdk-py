import itertools
import six


class PolylineCodec(object):
    def _pcitr(self, iterable):
        return six.moves.zip(iterable, itertools.islice(iterable, 1, None))

    def _write(self, output, value):
        coord = int(round(value * 1e5, 0))
        coord <<= 1
        coord = coord if coord >= 0 else ~coord

        while coord >= 0x20:
            output.write(six.unichr((0x20 | (coord & 0x1f)) + 63))
            coord >>= 5

        output.write(six.unichr(coord + 63))

    def _trans(self, value, index):
        byte, result, shift = None, 0, 0

        while (byte is None or byte >= 0x20):
            byte = ord(value[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            comp = result & 1

        return ~(result >> 1) if comp else (result >> 1), index

    def decode(self, expression):
        coordinates, index, lat, lng, length = [], 0, 0, 0, len(expression)

        while (index < length):
            lat_change, index = self._trans(expression, index)
            lng_change, index = self._trans(expression, index)
            lat += lat_change
            lng += lng_change
            coordinates.append((lat / 1e5, lng / 1e5))

        return coordinates

    def encode(self, coordinates):
        output = six.StringIO()
        self._write(output, coordinates[0][0])
        self._write(output, coordinates[0][1])

        for prev, curr in self._pcitr(coordinates):
            self._write(output, curr[0] - prev[0])
            self._write(output, curr[1] - prev[1])

        return output.getvalue()
