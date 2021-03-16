<a href="https://pandio.com"><img src="assets/pandio_225_blue-05.svg" alt="Pandio Logo"></a>

Learn more about Pandio at https://pandio.com

# Pandio Machine Learning

This repository contains the PandioML library and CLI tool to develop machine learning on the Pandio platform.

## Create a model in less than 1 minute!

1. `python pandioml/setup.py install`

2. `cd pandiocli && python setup.py install && cd ../`

3. `pandiocli register your@gmail.com`

4. `python examples/form_fraud/runner.py`

A graph showing the accuracy will be shown and the model will be saved as `form_fraud_example.model`

## Create a custom model in less than 10 minutes!

1. `python pandioml/setup.py install`

2. `cd pandiocli && python setup.py install && cd ../`

3. `pandiocli register your@gmail.com`

4. `pandiocli generate test_function`

5. `cd test_function`

6. Open `function.py` in your favorite editor, define methods `label_extraction` and `feature_extraction`

7. `python runner.py`

A graph showing the accuracy will be shown and the model will be saved as `test.model`

## Explore other datasets and models

