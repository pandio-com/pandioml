# Datasets

In PandioML datasets are how one would get data into a PandioML pipeline.

The general premise is, the dataset connects to a data source such as a database, csv file, or any other source of data, and streams it into a pipeline.

At the end of the day, this is just a Python class that implements a few methods.

1. `__init__`
1. `next`
1. `schema`

The `__init__` method establishes the connection to the data source and turns it into an iterable.

The `next` method iterates over the dataset and sets the data to a schema.

The `schema` method establishes the format of the data to ensure type safety for the pipeline.

Once the class is built, it can be tested and used locally with the `pandiocli` tool.

And once finished, this dataset can be deployed to the Pandio.com platform.

The design of these datasets were meant to work with anything that can be turned into an iterable. This could be an API, change data capture on a database, or anything one could turn into an iterable.