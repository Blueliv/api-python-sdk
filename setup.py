from setuptools import setup, find_packages

setup(
    name='blueliv-python-sdk',
    version='2.2.0',
    description='Blueliv API SDK for Python',
    url='https://github.com/Blueliv/api-python-sdk',
    author='Blueliv',
    author_email='community@blueliv.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='blueliv api crime servers bot ips security',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests>=2.4.0, <= 2.5.1', 'python-dateutil>=2.4.0'],
    test_requires=['mock']
)
