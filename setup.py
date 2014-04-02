import os
from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

VERSION = __import__('excel_sync').__version__

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-excel-sync",
    version=VERSION,
    packages=['excel_sync'],
    include_package_data=True,
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
