"""
Store some constants

"""
import numpy as np


ARRAY_LOC = {'MWA_128': ('-26.7033', '116.671', '377.830'),
             'VLA_D': ('34.025778', '252.3210278', '2125.3704')}
GHA = {'MWA_128': -7.778066666666667,
       'VLA_D': 16.821401853333334}

# MWA INFO
FIELD = {'EoR0': (0.0, -30.0),
         'EoR1': (4.0, -30.0),
         'EoR2': (10.33, -10.0)}
ZENITH = {'EoR0': (0.0, -26.7033),
          'EoR1': (4.0, -26.7033),
          'EoR2': (10.33, -26.7033)}

# MWA EoR central frequencies.
FREQ = {'EoR_low_40kHz': np.array([138.895 + 0.04 * i for i in range(704)]),
        'EoR_hi_40kHz': np.array([167.055 + 0.04 * i for i in range(705)]),
        'EoR_all_40kHz': np.array([138.895 + 0.04 * i for i in range(1409)]),
        'EoR_low_80kHz': np.array([138.915 + 0.08 * i for i in range(352)]),
        'EoR_hi_80kHz': np.array([167.075 + 0.08 * i for i in range(353)]),
        'EoR_all_80kHz': np.array([138.915 + 0.08 * i for i in range(705)]),
        '21cm':1420.40575177}