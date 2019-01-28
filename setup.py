import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-rotate-secret-key',
    version='0.3',
    packages=['rotatesecretkey'],
    description='Rotate your Django secret',
    long_description=README,
    author='Eralp Bayraktar',
    author_email='imeralpb@gmail.com',
    url='https://github.com/EralpB/django-rotate-secret-key/',
    license='MIT',
    install_requires=[
        'Django>=1.6',
    ]
)