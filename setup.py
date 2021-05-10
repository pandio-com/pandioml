import setuptools, os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="pandioml",
    version="1.0.4",
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
    ],
    install_requires=['numpy==1.20.1', 'pulsar-client==2.6.0', 'Faker==8.1.1', 'river==0.7.0', 'scikit-learn==0.24.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)