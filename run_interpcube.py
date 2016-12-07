"""
This script shows how to run interpcube in parallel using multiprocessing.

"""
from __future__ import print_function, division

import multiprocessing
from glob import glob

import numpy as np

from . import interpcube
from . import constants

lsize = 128
INDIR = '/data3/piyanat/model/21cm/original/'
OUTDIR = '/data3/piyanat/model/21cm/interpolated/'
zi, xi = np.genfromtxt(INDIR + 'delta_21cm_z_vs_xi.txt', unpack=True)
zi = zi[::-1] + 1
xi = xi[::-1]

cube = np.sort(glob(INDIR + 'delta_21cm_l{:d}_xi????.npy'.format(lsize)))[::-1]

freqlow = constants.FREQ['EoR_low_80kHz']
freqhi = constants.FREQ['EoR_hi_80kHz']
f21 = constants.FREQ['21cm'].value

zlow = f21 / freqlow - 1
zhi = f21 / freqhi - 1

freq = np.hstack((freqlow, freqhi))
z = np.hstack((zlow, zhi))

out = [OUTDIR + 'interp_delta_21cm_l{:d}_{:3.3f}MHz.npy'
       .format(lsize, f) for f in freq]


def run(args):
    i, o = args
    interpcube.interp_cube(i, zi=zi, cube=cube, outfile=o)


pool = multiprocessing.Pool(8)
pool.map(run, zip(z, out))
pool.close()
pool.join()
