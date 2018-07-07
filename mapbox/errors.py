
"""Errors raised by the Python SDK for Mapbox."""


class ValidationError(ValueError):
    """ValidationError

    ValidationError is the base class for 
    errors raised by the Python SDK for Mapbox.

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidCountryCodeError(ValidationError):
    """InvalidCountryCodeError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidPlaceTypeError(ValidationError):
    """InvalidPlaceTypeError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidProfileError(ValidationError):
    """InvalidProfileError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidFeatureError(ValidationError):
    """InvalidFeatureError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class HTTPError(ValidationError):
    """HTTPError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidCoordError(ValidationError):
    """InvalidCoordError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InputSizeError(ValidationError):
    """InputSizeError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class ImageSizeError(ValidationError):
    """ImageSizeError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class TokenError(ValidationError):
    """TokenError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidParameterError(ValidationError):
    """InvalidParameterError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidFileError(ValidationError):
    """InvalidFileError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidResourceTypeError(ValidationError):
    """InvalidResourceTypeError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidPeriodError(ValidationError):
    """InvalidPeriodError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidUsernameError(ValidationError):
    """InvalidUsernameError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidId(ValidationError):
    """InvalidId

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class MapboxDeprecationWarning(UserWarning):
    """MapboxDeprecationWarning

    The Python SDK for Mapbox raises this 
    warning when support for a particular service
    is coming to an end.

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidZoomError(ValidationError):
    """InvalidZoomError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidColumnError(ValidationError):
    """InvalidColumnError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidRowError(ValidationError):
    """InvalidRowError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidFileFormatError(ValidationError):
    """InvalidFileFormatError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidFeatureFormatError(ValidationError):
    """InvalidFeatureFormatError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidMarkerNameError(ValidationError):
    """InvalidMarkerNameError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidLabelError(ValidationError):
    """InvalidLabelError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass


class InvalidColorError(ValidationError):
    """InvalidColorError

    Parameters
    ----------
    message : str, optional
        A human-readable string describing the error.
    """

    pass
