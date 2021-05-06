import os

pandio = {
    'FUNCTION_NAME': 'exampleFunction123',
    'CONNECTION_STRING': 'pulsar://localhost:6651',
    'INPUT_TOPICS': ['non-persistent://public/default/in'],
    'OUTPUT_TOPICS': ['non-persistent://public/default/out'],
    'LOG_TOPIC': 'non-persistent://public/default/log',
    'ARTIFACT_STORAGE': f"{os.path.dirname(os.path.realpath(__file__))}/artifacts"
}
