# Contribution Guidelines

If you're planning on fixing a bug, or working on a relatively small contribution, generally you don't need to speak with anyone. It is advised to search through existing pull requests that are open to make sure someone else hasn't already made the same contribution.

If it is a larger feature, it is recommended to submit it as a discussion as a proposal to make sure it is something that will be accepted as a contribution.

## Workflow

1. Fork `pandio-com/pandioml`

1. Develop your changes on a branch from your fork

1. Commit and push changes to your local fork

1. Create a pull request on `pandio-com/pandioml` with your changes

## Local Development

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python3 -m venv /path/to/new/virtual/environment`

Two build scripts are included to quickly generate wheel files and install locally.

From project root:

`cd pandioml && ./build.sh && cd ../ && cd pandiocli && ./build.sh && cd ../`

Optionally, you can also build the EGG files locally yourself for hot reloading of project files.

## Datasets and Generators

When adding a dataset or generator, please make sure to add a docstring. See existing classes for an example.

## Lastly...

A big **thank you** for considering contributing to this project.

Open source is a beautiful thing!