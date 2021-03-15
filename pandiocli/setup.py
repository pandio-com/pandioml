import setuptools

setuptools.setup(
    name="pandiocli",
    version="1.0.0",
    author="Joshua Odmark",
    author_email="josh@pandio.com",
    description="CLI to control Pandio's machine learning service.",
    long_description="CLI to control Pandio's machine learning service.",
    # change below if readme is not written in markdown
    long_description_content_type="text/markdown",
    url="https://github.com/pandio-com/pandioml",  # usually to github repository
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    entry_points={
        "console_scripts": [
            'pandiocli = src.__main__:main'
        ]
    }
)