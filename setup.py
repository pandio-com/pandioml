import setuptools, os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pandioml/requirements.txt'), "r")
_reqs = f.read().splitlines()

INSTALL_REQUIRES = _reqs
EXTRAS_REQUIRE = {
    "pulsar": ['pulsar-client==2.7.2']
}

setuptools.setup(
    name="pandioml",
    version="1.0.9",
    author="Joshua Odmark",
    author_email="josh@pandio.com",
    description="Pandio's machine learning library.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pandio-com/pandioml",
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=" ".join(
        [
            "machine learning",
            "data science",
            "pandio",
            "artificial intelligence",
            "build models",
            "online machine learning",
            "streaming",
            "classifiers",
            "supervised learning",
            "regressions",
        ]
    ),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
