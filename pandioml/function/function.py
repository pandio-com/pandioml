"""function.py: This is the core interface of the function api.
# The process method is called for every message of the input topic of the
# function. The incoming input bytes are deserialized using the serde.
# The process function can optionally emit an output
"""
from abc import abstractmethod


class Function(object):
    """Interface for Pulsar Function"""
    @abstractmethod
    def process(self, input, context):
        """Process input message"""
        pass


class Context:
    _data = {}

    def get_logger(self):
        return Logger()

    def put_state(self, key, value):
        self._data[key] = value

    def get_state(self, key):
        return self._data[key]


class Logger():
    def info(self, message):
        print(message)

    def error(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def debug(self, message):
        print(message)


# class ContextImpl(pulsar.Context):
#   def get_message_id(self):
#     ...
#   def get_message_key(self):
#     ...
#   def get_message_eventtime(self):
#     ...
#   def get_message_properties(self):
#     ...
#   def get_current_message_topic_name(self):
#     ...
#   def get_partition_key(self):
#     ...
#   def get_function_name(self):
#     ...
#   def get_function_tenant(self):
#     ...
#   def get_function_namespace(self):
#     ...
#   def get_function_id(self):
#     ...
#   def get_instance_id(self):
#     ...
#   def get_function_version(self):
#     ...
#   def get_logger(self):
#     ...
#   def get_user_config_value(self, key):
#     ...
#   def get_user_config_map(self):
#     ...
#   def record_metric(self, metric_name, metric_value):
#     ...
#   def get_input_topics(self):
#     ...
#   def get_output_topic(self):
#     ...
#   def get_output_serde_class_name(self):
#     ...
#   def publish(self, topic_name, message, serde_class_name="serde.IdentitySerDe",
#               properties=None, compression_type=None, callback=None, message_conf=None):
#     ...
#   def ack(self, msgid, topic):
#     ...
#   def get_and_reset_metrics(self):
#     ...
#   def reset_metrics(self):
#     ...
#   def get_metrics(self):
#     ...
#   def incr_counter(self, key, amount):
#     ...
#   def get_counter(self, key):
#     ...
#   def del_counter(self, key):
#     ...
#   def put_state(self, key, value):
#     ...
#   def get_state(self, key):
#     ...