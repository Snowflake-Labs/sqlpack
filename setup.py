from distutils.core import setup
from setuptools import find_packages

setup(
    name='sqlpack',
    packages=['sqlpack'],
    version='0.1',
    license='OSI Approved :: Apache Software License',
    description='The sqlpack module lets you distribute modular SQL code.',
    author='Siddhil Rathod',
    author_email='siddhi.rathod@snowflake.com',
    url='https://github.com/Snowflake-Labs/sqlpack',
    download_url='https://github.com/Snowflake-Labs/sqlpacks/archive/refs/tags/0.1.0.tar.gz',
    scripts=['bin/sqlpack'],
    package_data={"sqlpack": ["*.py", "../packs/*/main.sql.fmt", "../packs/*/*.yaml"]},
    include_package_data=True,
    keywords='SNOWFLAKE PACKS SNOWSQL SNOWSQL-PACKS',
    install_requires=[
        'fire',
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
    ],
)
