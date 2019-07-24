import os
from setuptools import find_packages, setup

install_requires = []
README = None

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as req:
    install_requires = list(req.read().splitlines())

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='scrapyd-dash',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A dashboard for scrapy project using scrapyd and logparser',
    install_requires=install_requires,
    long_description=README,
    url='https://github.com/Dainius-P/scrapyd-dash',
    author='Dainius Preimantas',
    author_email='preimantasd@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
