from abc import abstractmethod
import os


class Function(object):
    """Interface for Pulsar Function"""
    @abstractmethod
    def process(self, input, context):
        """Process input message"""
        pass


class Context:
    _data = {
        '_user': {}
    }

    def set_user_config_value(self, key, value):
        self._data['_user'][key] = value

    def get_user_config_value(self, key):
        if key in self._data['_user']:
            return self._data['_user'][key]
        else:
            return None

    def get_user_config_map(self):
        return self._data['_user']

    def get_logger(self):
        return Logger()

    def put_state(self, key, value):
        if not isinstance(value, str):
            raise Exception(f"Value passed in to store is not a string.")
        f = open(f"/tmp/{key}", "w")
        f.write(value)
        f.close()

    def get_state(self, key):
        if os.path.exists(f"/tmp/{key}"):
            f = open(f"/tmp/{key}", "r")
            data = f.read()
            f.close()
            return data

        return None

    def get_counter(self, key):
        try:
            return self._data[key]
        except:
            return None

    def del_counter(self, key):
        return self._data.pop(key, None)

    def incr_counter(self, key, amount):
        if key not in self._data:
            self._data[key] = amount
        else:
            self._data[key] += amount

    def publish(self, topic_name, message, serde_class_name="serde.IdentitySerDe",
                              properties=None, compression_type=None, callback=None, message_conf=None):
        print(f"Simulating putting {message} on topic {topic_name}")
        if callable(callback):
            callback()


class Logger:
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
#   def put_state(self, key, value):
#     ...
#   def get_state(self, key):
#     ...