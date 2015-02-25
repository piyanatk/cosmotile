import numpy as np
from multiprocessing import Pool
from routines.cube2hpx import cube2hpx
from glob import glob
from api import settings


# freqs = np.hstack((settings.FREQ['EoR_low_80kHz'],
#                   settings.FREQ['EoR_hi_80kHz']))
freqs = settings.FREQ['EoR_hi_80kHz']
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
