from setuptools import setup, find_packages

def get_long_description():
    with open('README.md') as f:
        return f.read()

setup(
    name='blockpype',
    version='1.0.0a2',

    description="Breaks apart input stream into blocks and pipes each block into newly spawned processes",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    url='https://github.com/kfzteile24/blockpype',

    install_requires=[
    ],

    python_requires='~=3.6',

    dependency_links=[
    ],

    #extras_require={
    #    'test': ['pytest', 'pytest_click'],
    #},

    packages=find_packages(),

    author='kfzteile24 GmbH',
    license='MIT',

    entry_points={
        'console_scripts': [
            'blockpype = blockpype.cli:main',
        ],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    keywords=[
        'pipe split buffer block streaming'
    ]
)
