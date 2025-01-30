from setuptools import setup, find_packages

import django_postgres_extensions

setup(name='django-postgres-extensions',
    version=django_postgres_extensions.__version__,
    description="Extra features for django.contrib.postgres",
    long_description=open('description.rst').read(),
    author='SoulString',
    author_email='mike@soulstring.io',
    url='https://github.com/zmey3301/django_postgres_extensions',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'Django>=4.0',
        'six'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
