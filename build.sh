pip install wheel

pip uninstall pandioml -y

python setup.py bdist_wheel

pip install dist/pandioml-1.0.12-py3-none-any.whl