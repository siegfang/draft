__author__ = 'fangy'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import numpy

extensions = [
    Extension("my_app", ["my_app.pyx"],
              include_dirs=[numpy.get_include()])
]
setup(
    name="my_app",
    ext_modules=cythonize(extensions),
)
