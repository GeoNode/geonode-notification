from setuptools import setup, find_packages


setup(
    name="geonode-notification",
    version=__import__("notification").__version__,
    description="User notification management for the Django web framework",
    long_description=open("docs/usage.rst").read(),
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    url="https://github.com/GeoNode/geonode-notification",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Framework :: Django",
    ],
    include_package_data=True,
    test_suite='runtests',
    install_requires=[
        'django>=1.4',
    ],
    zip_safe=False,
)
