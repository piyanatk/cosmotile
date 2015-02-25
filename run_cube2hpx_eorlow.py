"""
This script shows how to run cube2hpx in parallel using multiprocessing module.

"""
from multiprocessing import Pool

from .cube2hpx import cube2hpx
from . import constants


freqs = constants.FREQ['EoR_low_80kHz']
cube_dir = '/data3/piyanat/model/21cm/interpolated/'
hpx_dir = '/data3/piyanat/model/21cm/healpix/'
cubefiles = [cube_dir + 'interp_delta_21cm_l128_{:.3f}MHz.npy'
             .format(f) for f in freqs]
hpxfiles = [hpx_dir + 'hpx_interp_delta_21cm_l128_{:.3f}MHz.fits'
            .format(f) for f in freqs]


def call_cube2hpx(args):
    print args
    cube, hpx, f = args
    cube2hpx(cube, hpx, f)


workers = Pool(8)
workers.map(call_cube2hpx, zip(cubefiles, hpxfiles, freqs))
workers.close()
workers.join()
