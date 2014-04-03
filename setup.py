import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

VERSION = __import__('excel_sync').__version__

EXCLUDE_FROM_PACKAGES = []

REQUIRES = [
    'Django==1.6.2',
    'mock==1.0.1',
    'mockito==0.5.2',
    'xlrd==0.9.2'
]

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-excel-sync",
    version=VERSION,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    install_requires=REQUIRES,
    license='BSD',
    description='A Django app to synchronize data between Excel files and Django Models',
    long_description=README,
    url='https://github.com/FriedrichK/django-excel-sync',
    author='Friedrich Kauder',
    author_email='fkauder@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
