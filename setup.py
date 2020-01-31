"""PyPI setup script for the django-flexible-subscriptions package."""
# pylint: disable=line-too-long
from setuptools import find_packages, setup

from subscriptions import __version__

with open('README.rst', 'r') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name='django-flexible-subscriptions',
    version=__version__,
    url='https://github.com/studybuffalo/django-flexible-subscriptions',
    description=('A subscription and recurrent billing application for Django.'),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    author='Joshua Torrance',
    author_email='studybuffalo@gmail.com',
    keywords='Django, subscriptions, recurrent billing',
    platforms=['linux', 'windows'],
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    package_data={
        'subscriptions': [
            'static/subscriptions/*.css',
            'templates/subscriptions/*.html',
            'templates/subscriptions/snippets/*.html',
        ]
    },
    project_urls={
        'Documentation': 'https://django-flexible-subscriptions.readthedocs.io/en/latest/',
        'Source code': 'https://github.com/studybuffalo/django-flexible-subscriptions',
        'Issues': 'https://github.com/studybuffalo/django-flexible-subscriptions/issues',
    },
    python_requires='>=3.5',
    install_requires=[
        'django>=1.11',
    ],
    tests_require=[
        'pytest==5.3.5',
        'pytest-cov==2.8.1',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Other/Nonlisted Topic'
    ],
)
