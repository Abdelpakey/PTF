from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np

'''
SET VS90COMNTOOLS=%VS100COMNTOOLS%
python setup_cython_old.py build_ext --inplace
python ImageDirectoryTracking.py --esm "G:\UofA\Thesis\#Code\Datasets\Human\nl_bookI_s3\*.jpg" Results
'''

setup(
    name="Cython Tracker Library",
    cmdclass={'build_ext': build_ext},
    include_dirs=[np.get_include()],
    ext_modules=[
        Extension("cython_trackers_old.utility", ["cython_trackers_old/utility.pyx"]),
        Extension("cython_trackers_old.ESMTracker", ["cython_trackers_old/ESMTracker.pyx"]),
        Extension("cython_trackers_old.BMICTracker", ["cython_trackers_old/BMICTracker.pyx"]),
        Extension("cython_trackers_old.NNTracker", ["cython_trackers_old/NNTracker.pyx"])
    ]
)
    
