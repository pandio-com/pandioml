import setuptools, os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    'numpy==1.20.1',
    'Faker==8.1.1',
    'river==0.7.0',
    'scikit-learn==0.24.1',
    'pandiocli==1.0.9',
    'cloudstorage==0.11.0',
    'cloudstorage[amazon]==0.11.0',
    'cloudstorage[google]==0.11.0',
    'six==1.16.0'
]
EXTRAS_REQUIRE = {
    "pulsar": ['pulsar-client==2.7.1']
}

setuptools.setup(
    name="pandioml",
    version="1.0.5",
    author="Joshua Odmark",
    author_email="josh@pandio.com",
    description="Pandio's machine learning library.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pandio-com/pandioml",
    packages=setuptools.find_packages(exclude=['tests']),
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
            "storage",
            "amazon",
            "aws",
            "s3",
            "azure",
            "rackspace",
            "cloudfiles",
            "google",
            "cloudstorage",
            "gcs",
            "minio",
        ]
    ),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
