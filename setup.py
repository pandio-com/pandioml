import setuptools

setuptools.setup(
    name="pandioml",
    version="1.0.0",
    author="Joshua Odmark",
    author_email="josh@pandio.com",
    description="Pandio's machine learning library.",
    long_description="Pandio's machine learning library.",
    # change below if readme is not written in markdown
    url="https://github.com/pandio-com/pandioml",  # usually to github repository
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    # For Testing
    # install_requires=['numpy==1.20.1', 'pulsar-client==2.6.0', 'Faker==8.1.1',
    #                  'river @ git+https://github.com/pandio-com/river@0.7.0#egg=river'],
    # For Release
    install_requires=['numpy==1.20.1', 'pulsar-client==2.6.0', 'Faker==8.1.1', 'river==0.7.0', 'scikit-learn==0.24.1'],
    # For PandioCLI
    # install_requires=['numpy==1.20.1', 'Faker==8.1.1', 'river==0.7.0', 'scikit-learn==0.24.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)