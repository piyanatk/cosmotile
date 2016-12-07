"""
Program: hpx2sin.py
    Perform gridding of a HEALPix map into a SIN projected FITS images.
Author: Piyanat Kittiwisit
        piyanat.kittiwisit@asu
Create: August 19, 2013

"""
from __future__ import print_function, division

import argparse
from datetime import datetime

import numpy as np
import healpy as hp
from astropy import wcs
from astropy.io import fits


def hpx2sin(hpxfile, fitsfile, ra, dec, size=7480, res=0.015322941176470588,
            hpx_coord='C', hpx_array=None, hpx_multiplier=1, hdr=None):
    """
    Generate a SIN (orthographic) projected FITS images from a HEALPix image.

    Parameters
    ----------
    hpxfile: string
        Name of the input Healpix file.
    fitsfile: string
        Name of the output FITS images
    ra: float, range=[0,360]deg
        Right ascension at the center of the FITS images.
    dec: float, range=[90,-90]deg
        Declination at the center of the FITS images.
    size: integer, optional
        Size of the output FITS image in number of pixels. Default = 7480.
        Only support a square image.
    res: float, optional
        Angular resolution at the center pixel of the FITS image in degree
    hpx_coord : {'C', 'E' or 'G'}, optional
        The coordinates of the healpix map.
        'C' for Celestial (default), 'E' for Ecliptic, and 'G' for Galactic.
    hpx_array: array-like or None, optional
        Array of Healpix pixels.
        If provide, this array will be used instead of reading an array
        from hpxfile. hpxfile will still be used as a reference filename.
    hpx_multiplier: float, optional
        Multiplier to the healpix map before gridding.
    hdr: dict
        Additional FITS header to apply to the output FITS image.
        hdr=dict(KEYWORD1=value1,KEYWORD2=value2, ...), or
        hdr=dict(KEYWORD1=(value1, comment1), KEYWORD2=(value2, comment2), ...)

    Note
    ----
    The default combination of `size` and `res` give a half-sky SIN
    image with ~0.9" resolution, suitable for MWA simulation in MAPS.


    """
    print('hpx2sin {:s} {:s} {:.3f} {:.3f} {:d} {:f}'
          .format(hpxfile, fitsfile, ra, dec, size, res))
    if not hpx_array:
        hpx_array, hpx_hdr = hp.read_map(hpxfile, h=True)
    if not hp.isnpixok(len(hpx_array)):
        raise IOError('Number of pixels in a healpix array '
            'must be 12 * nside ** 2.')

    # Create a new WCS object and set up a SIN projection.
    w = wcs.WCS(naxis=2)
    w.wcs.crpix = [float(size / 2), float(size / 2)]
    w.wcs.cdelt = [-res, res]
    w.wcs.crval = [ra, dec]
    w.wcs.ctype = ["RA---SIN", "DEC--SIN"]
    w.wcs.cunit = ['deg', 'deg']
    w.wcs.equinox = 2000.0

    # Write out the WCS object as a FITS header, adding additional
    # fits keyword as applied.
    header = w.to_header()
    header['DATE'] = (datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
                      'Date of file creation')
    # TODO: This program should keep history from healpix file
    header['HISTORY'] = 'hpx2sin hpxfile fitsfile ra dec size res'
    header['HISTORY'] = 'hpx2sin {:s} {:s} {:.3f} {:.3f} {:d} {:f}'\
        .format(hpxfile, fitsfile, ra, dec, size, res)
    if hdr:
        for key, value in hdr.iteritems():
            header[key] = value

    # Some pixel coordinates of interest.
    x, y = np.mgrid[0:size, 0:size]

    # Convert pixel coordinates to celestial world coordinates
    pixra, pixdec = w.wcs_pix2world(x.ravel(), y.ravel(), 0)
    pixra *= np.pi / 180.
    pixdec = np.pi * (90 - pixdec) / 180.  # Healpix dec is 0 to pi.
    valid_pix = np.logical_not(np.isnan(pixra))

    # Perform coordinate transformation if needed. Convert celestial world
    # coordinates to the Healpix world coordinates to grab the right
    # Healpix pixels.
    if hpx_coord != 'C':
        rot = hp.Rotator(coord=['C', hpx_coord])
        pixdec[valid_pix], pixra[valid_pix] = \
            rot(pixdec[valid_pix], pixra[valid_pix])

    # Get the pixel value from the HEALPix image
    proj_map = np.zeros(size * size)
    proj_map[valid_pix] = hp.get_interp_val(hpx_multiplier * hpx_array,
                                            pixdec[valid_pix],
                                            pixra[valid_pix])

    # Make a HDU object and save the FITS file. Axes in 2D numpy array are
    # ordered slow then fast, opposite to ordering in FITS convention, so
    # we have to save the transposed image array.
    hdu = fits.PrimaryHDU(data=proj_map.reshape((size, size)).T, header=header)
    hdu.writeto(fitsfile, clobber=True)


# Command-line paarsing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a SIN (orthographic) projected FITS images from '
                    'a HEALPix image.')
    parser.add_argument('hpxfile', type=str,
                        help='Path to an input HEALPix file')
    parser.add_argument('fitsfile', type=str,
                        help='Path to an output FITS image')
    parser.add_argument('ra', type=float,
                        help='Right ascension at the center of the projected '
                             'images. range=[0,360]deg')
    parser.add_argument('dec', type=float,
                        help='Declination at the center of the projected '
                             'images. range=[90,-90]deg')
    parser.add_argument('-s', '--size', type=int, default=7480,
                        help='Size of the projected image in pixels. '
                             'Only support square images.')
    parser.add_argument('-r', '--res', type=float, default=0.015322941176470588,
                        help='Angular resolution at the center pixel of the '
                             'projected image in degree.')
    parser.add_argument('-c', '--coord', '--hpx_coord', type=str, default='C',
                        help="The coordinate of the HEALPix map."
                             "'E' for Ecliptic, 'G' for Galactic and "
                             "'C' for Celestial (default).")
    parser.add_argument('-m', '--multiplier', type=float, default=1,
                        help="Multiplier to HEALPix map before gridding.")
    args = parser.parse_args()
    hpx2sin(args.hpxfile, args.fitsfile, args.ra, args.dec, size=args.size,
            res=args.res, hpx_coord=args.coord, hpx_multiplier=args.multiplier)
