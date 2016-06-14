import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='security-sensor',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='Security sensor is a Django app to process events log from different security source.',
    long_description=README,
    url='https://www.example.com/',
    author='Moises Gautier Gomez',
    author_email='moisesgautiergomez@correo.ugr.es',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9.2',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'Intended Audience :: DevOps',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: Iptables :: Events log',
        'Topic :: Internet :: Security networks',
    ],
)
