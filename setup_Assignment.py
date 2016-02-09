from __future__ import division, print_function, absolute_import
import sys
sys.dont_write_bytecode = True

import numpy as np
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


import subprocess
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True




setup(
      cmdclass={'build_ext': build_ext},
      ext_modules = [
              Extension("AoN",
                        ["AoN.pyx"],
                        include_dirs=[np.get_include()])
                    ]
     )

