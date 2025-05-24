from setuptools import setup
from Cython.Build import cythonize

setup(
    name='mov-detection',
    version='1',
    packages=['src'],
    url='',
    license='',
    author='',
    author_email='',
    description='',
    ext_modules=cythonize("src/bounding.pyx")
)
