"""
WTForms-MongoEngine
--------------

WTForms extensions for Mongoengine.

It's a fork of Flask-Mongoengine, but Flask depedencies were removed.
"""
from setuptools import setup

# Stops exit traceback on tests
try:
    import multiprocessing
except:
    pass

setup(
    name='wtforms-mongoengine',
    version='0.1',
    url='https://github.com/snahor/wtforms-mongoengine',
    license='BSD',
    description='WTForms extension for mongoengine',
    author="Hans Roman",
    author_email="hans@roman.pe",
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'mongoengine>=0.8.2',
        'wtforms>=1.0.4',
    ],
    packages=['wtforms_mongoengine'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
