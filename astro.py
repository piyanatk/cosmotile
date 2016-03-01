"""
Routines for astronomical related calculation.

"""
import datetime

import numpy as np

import astropy.units as u


def beam_area(*args):
    """
    Calculate the Gaussian beam area.

    Parameters
    ----------
    args: float
        Beam widths.
        If args is a single argument, a symmetrical beam is assumed.
        If args has two arguments, the two arguments are bmaj and bmin,
        the width of the major and minor axes of the beam in that order.

    Return
    ------
    out: float
        Beam area. No unit conversion is performed, i.e. the unit will depend
        on the input arguments. For example, beam width in degree wil return
        the beam area in square degree. Likewise, beam width in pixel will
        return the beam area in pixel.

    """
    if len(args) > 2:
        raise ValueError('Input argument must be a single beam width for a '
                         'symmetrical beam, or widths of the major and minor '
                         'axes of the beam.')
    if len(args) == 2:
        bmaj, bmin = args
    else:
        bmaj = args[0]
        bmin = bmaj
    return np.pi * bmaj * bmin / (4 * np.log(2))


def jysr2k(intensity, freq):
    """
    Convert Jy/sr to K.

    Parameters
    ----------
    intensity: array-like
        Intensity (brightness) in Jy/sr
    freq: float
        Frequency of the map in MHz

    Return
    ------
    out: array-like or float
        Brightness temperature in Kelvin


    """
    ba = 1 * u.sr
    equiv = u.brightness_temperature(ba, freq * u.MHz)
    return (intensity * u.Jy).to(u.K, equivalencies=equiv).value


def k2jysr(temp, freq):
    """
    Convert K to Jy/sr.

    Parameters
    ----------
    temp: array-like
        Brightness temperature in Kelvin
    freq: float
        Frequency of the map in MHz

    Return
    ------
    out: array-like or float
        Intensity (brightness) in Jy/sr

    """
    ba = 1 * u.sr
    equiv = u.brightness_temperature(ba, freq * u.MHz)
    return (temp * u.K).to(u.Jy, equivalencies=equiv).value


def jybeam2k(intensity, freq, beam_width):
    """
    Convert Jy/beam to K.

    Parameters
    ----------
    intensity: array-like
        Intensity (brightness) in Jy/beam
    freq: float
        Frequency of the map in MHz
    beam_width: float
        The Gaussian beam width in degree

    Return
    ------
    out: array-like or float
        Brightness temperature in Kelvin

    """
    ba = beam_area(beam_width) * u.Unit('deg2')
    equiv = u.brightness_temperature(ba, freq * u.MHz)
    return (intensity * u.Jy).to(u.K, equivalencies=equiv).value


def k2jybeam(temp, freq, beam_width):
    """
    Convert K to Jy/beam.

    Parameters
    ----------
    temp: array-like
        Brightness temperature in Kelvin
    freq: float
        Frequency of the map in MHz
    beam_width: float
        The Gaussian beam width in degree

    Return
    ------
    out: array-like or float
        Intensity (brightness) in Jy/beam

    """
    ba = beam_area(beam_width) * u.Unit('deg2')
    equiv = u.brightness_temperature(ba, freq * u.MHz)
    return (temp * u.K).to(u.Jy, equivalencies=equiv).value
