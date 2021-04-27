# Quick Start

## Create a custom model in less than 10 minutes!

1. `cd pandioml && ./build.sh && cd ../`

1. `cd pandiocli && ./build.sh && cd ../`

1. `pandiocli register your@gmail.com`

1. `pandiocli generate test_function`

1. Open `fnc.py` in your favorite editor, put your pipelines code in the `pipelines` method.

1. `pandiocli test --project_folder test_function --dataset_name FormSubmissionGenerator --loops 100`

      FormSubmissionGenerator is used in this example, but any dataset or generator from `pandioml.data.*` can be used. Or you can build your own as described below.

A graph showing the model accuracy will be generated after running the example.

*Tip: Open up an example `fnc.py` to get a jumpstart inside one of the examples in the `./examples` directory*