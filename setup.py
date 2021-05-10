import setuptools, os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt')) as f:
    required = f.read().splitlines()

setuptools.setup(
    name="pandioml",
    version="1.0.2",
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
    install_requires=required,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)