"""
This script shows how to run hpx2sin in parallel using multiprocessing module.

"""
import multiprocessing

import numpy as np
import healpy as hp

import modules.settings as s
from routines.hpx2sin import hpx2sin


# Frequency information
# freqs = np.hstack((s.FREQ['EoR_low_80kHz'], s.FREQ['EoR_hi_80kHz']))
freqs = s.FREQ['EoR_low_80kHz']

# Pointing information
fov_ra, fov_dec = s.ZENITH['EoR0']

# Snapshot coordinates
ha = 0.
ra = fov_ra + ha
dec = fov_dec


# Caller function.
def run_hpx2sin(args):
    infile, outfile = args
    hpx2sin(infile, outfile, ra, dec, hpx_coord='C')


hpxdir = '/data3/piyanat/model/21cm/healpix/'
hpxfile = ['{:s}hpx_interp_delta_21cm_l128_{:.3f}MHz.npy'
    .format(hpxdir, f) for f in freqs]
fitsdir = '/data3/piyanat/model/21cm/sin/'
fitsfile = ['{:s}sin_interp_delta_21cm_l128_0.000h_{:.3f}MHz.fits'
    .format(fitsdir, f) for f in freqs]

pool = multiprocessing.Pool(8)
pool.map(run_hpx2sin, zip(hpxfile, fitsfile))
pool.close()
pool.join()
