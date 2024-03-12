from setuptools import setup, find_packages


setup(
    name='ezpylog',
    version='2.2.0',
    license='GPLv3',
    author="Jérémie Rodez",
    author_email='jeremierodez@outlook.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/JRodez/ezpylog',
    keywords='tool print ezpylog logger logging log level debug info warning error critical color terminal cli magnificient colorful beautiful filter filter_by_level filter_by_context filter_by_message',
    install_requires=[
        # 'enum', 'datetime'
    ], classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

)
