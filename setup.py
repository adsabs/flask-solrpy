"""
Flask-solrpy
-------------

Flask extension for the solrpy library: http://pypi.python.org/pypi/solrpy/
"""
from setuptools import setup

setup(
    name='Flask-Solrpy',
    version='0.1',
    url='http://github.com/flask-solrpy',
    license='MIT',
    author='Jay Luker',
    author_email='jay.luker@gmail.com',
    description='A Flask extension for the solrpy library',
    long_description=__doc__,
    py_modules=['flask_solrpy'],
    install_requires=[
        'Flask',
        'solrpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries'
        ],
)