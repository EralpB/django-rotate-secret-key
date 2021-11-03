import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-rotate-secret-key',
    version='0.3',
    packages=find_packages(exclude=['tests']),
    description='Rotate your Django secret',
    long_description=README,
    author='Eralp Bayraktar',
    author_email='imeralpb@gmail.com',
    url='https://github.com/EralpB/django-rotate-secret-key/',
    license='MIT',
    install_requires=[
        'Django>=2.2',
    ]
)