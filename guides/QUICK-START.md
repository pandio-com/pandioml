# Quick Start

## Create a custom model in less than 30 minutes!

1. `pip install pandioml`

1. `pandiocli register your@gmail.com`

1. `pandiocli function generate --project_name test_function`

1. Open `test_function/function.py` in your favorite editor, put your pipelines code in the `pipelines` method.

1. `pandiocli test --project_folder test_function --dataset_name FormSubmissionGenerator --loops 100`

      FormSubmissionGenerator is used in this example, but any dataset or generator from `pandioml.data.*` can be used. Or you can build your own as described below.

*Tip: Open up an example `function.py` to get a jumpstart inside one of the examples in the [/examples](./../examples) directory*