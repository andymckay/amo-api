from setuptools import setup


setup(
    name='amo-api',
    version='0.1',
    description='addons.mozilla.org API',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    install_requires=['requests',
                      'mock'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
        ],
    )
