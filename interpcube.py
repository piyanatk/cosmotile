"""
Program: interpcube.py
    Perform linear interpolation between 21 cm simulation cubes.
Author: Piyanat Kittiwisit
        piyanat.kittiwisit@asu
Create: August 19, 2013

"""
from __future__ import print_function, division

import numpy as np
import argparse


def interpolate(arr1, arr2, z1, z2, z):
    """
    Perform linear interpolation via weighted average.

    """
    # TODO: Check if arr1 and arr2 have the same shape?
    arr_shape = arr1.shape
    w1 = (z2 - z) / (z2 - z1)
    w2 = (z - z1) / (z2 - z1)
    return np.average(np.vstack((arr1.ravel(), arr2.ravel())), axis=0,
                      weights=(w1, w2)).reshape(arr_shape)


def interp_cube(z, zi=None, cube=None, read_from=None, outfile=None):
    """
    Perform pixel-wise linear interpolation between simulation cubes to the
    redshift of interest.

    Parameters
    ----------
    z: float or integer
        Redshift of interest to interpolate from cubes.
    zi: array of float or None
        Redshift associated with simulation cubes. Must be sorted in ascending
        order. Use default set of redshift and cubes if both are None.
    cube: array of string or None
        Path to simulation cubes in numpy binary file format (*.npy).
        Use default set of redshift and cubes if both are None.
    read_from: string
        Path to a file containing comma-separated set of zi and cube to read
        from. Overwrite zi and cube parameters.
    outfile: string
        Path to an output file.

    """
    assert isinstance(z, (float, int)), 'Can only interpolate to 1 z at a time.'
    if read_from is not None:
        zi, cube = np.genfromtxt(read_from, delimiter=',')
    elif zi is None and cube is None:
        # Load default.
        zi = np.array([6.26864407, 6.58384245, 6.92248825, 7.51166288])
        cube = np.array(['ComovingCube_XHI11.npy',
                         'ComovingCube_XHI21.npy',
                         'ComovingCube_XHI32.npy',
                         'ComovingCube_XHI49.npy'])
    else:
        assert hasattr(zi, '__iter__') and hasattr(cube, '__iter__'),\
            'Only one pair of zi and cube is given. Need more to interpolate.'
        # TODO: Need to find a way to return the given cube for the above case?
        assert len(zi) == len(cube), 'zi and cube must have the same length.'
    # TODO: sort zi and cube to remove restriction on inputs.

    # Perform interpolation.
    # Case 1: Exact match.
    if z in zi:
        icube = np.load(cube[np.where(z == zi)])
    # Case 2: Out of lower bound.
    elif np.all(z < zi):
        icube = np.load(cube[0])
    # Case 3: Out of upper bound.
    elif np.all(z > zi):
        icube = np.load(cube[-1])
    # Case 4: Interpolate from two neighboring cubes.
    else:
        # TODO: np.searchsorted only work with zi in ascending order. Must fix.
        i = int(np.searchsorted(zi, z))
        icube = interpolate(np.load(cube[i - 1]),
                            np.load(cube[i]),
                            zi[i - 1], zi[i], z)
    if outfile is None:
        outfile = 'interp_cube_z{:.3f}.npy'.format(z)
    np.save(outfile, icube)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('z', type=float,
                        help='Redshift of interest to interpolate from cubes.')
    parser.add_argument('--zi', type=float, nargs='*',
                        help='Redshift associated with simulation cubes. Must '
                             'be sorted in ascending order. Use default set of '
                             'redshift and cubes if both are None.')
    parser.add_argument('--cube', type=str, nargs='*',
                        help='Path to simulation cubes in numpy binary file '
                             'format (*.npy). The files should contain record '
                             'arrays with temp columns. Use default set of '
                             'redshift and cubes if both are None.')
    parser.add_argument('--read_from', type=str,
                        help='Path to a file containing comma-separated set of '
                             'zi and cube to read from. Overwrite zi and cube '
                             'parameters.')
    parser.add_argument('--outfile', type=str,
                        help='Path to an output file.')
    args = parser.parse_args()
    interp_cube(args.z, zi=args.zi, cube=args.cube, read_from=args.read_from,
                outfile=args.outfile)
