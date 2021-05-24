from pandioml.data.stream import Stream
import pulsar
from pandioml.data.record import JsonSchema, Record, Float, Integer


class WebHostingDataset(Stream):
    """
    Contains 12,496,728 server resource metric events recorded over a 3 month period of time.

    Each record is an instance of ResourceEvent

    class ResourceEvent(Record):
        cpu_usage_mhz = Float()
        cpu_usage_percent = Float()
        cpu_provisioned_mhz = Float()
        ingress_bandwidth_kbs = Float()
        egress_bandwidth_kbs = Float()
        memory_kb = Float()
        timestamp_ms = Integer()
        weekday = Integer()
        weekend = Integer()
        month = Integer()
        day = Integer()
        hour = Integer()
        cpu_prev_usage_percent = Float()
        cpu_diff_usage_percent = Float()
        ingress_bandwidth_prev_kbs = Float()
        ingress_bandwidth_diff_kbs = Float()
        egress_bandwidth_prev_kbs = Float()
        egress_bandwidth_diff_kbs = Float()
    """

    index = 0
    dataset = None

    def __init__(self, start_id=pulsar.MessageId.earliest, receiver_queue_size=1000, pandio_token=None):
        self.client = pulsar.Client('pulsar+ssl://joshuaeric--gray-guan.us-west2.gcp.pulsar.pandio.com:6651',
                       authentication=pulsar.AuthenticationToken(pandio_token))

        self.reader = self.client.create_reader('persistent://public/default/shared-webhost', start_id,
                                                schema=JsonSchema(ResourceEvent),
                                                receiver_queue_size=receiver_queue_size)

    def next(self):
        msg = self.reader.read_next()
        self.index += 1
        return msg

    @staticmethod
    def schema():
        return JsonSchema(ResourceEvent)


class ResourceEvent(Record):
    cpu_usage_mhz = Float()
    cpu_usage_percent = Float()
    cpu_provisioned_mhz = Float()
    ingress_bandwidth_kbs = Float()
    egress_bandwidth_kbs = Float()
    memory_kb = Float()
    timestamp_ms = Integer()
    weekday = Integer()
    weekend = Integer()
    month = Integer()
    day = Integer()
    hour = Integer()
    cpu_prev_usage_percent = Float()
    cpu_diff_usage_percent = Float()
    ingress_bandwidth_prev_kbs = Float()
    ingress_bandwidth_diff_kbs = Float()
    egress_bandwidth_prev_kbs = Float()
    egress_bandwidth_diff_kbs = Float()
