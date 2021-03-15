from skmultiflow.data.base_stream import Stream
import faker


class FormSubmissionGenerator(Stream):

    def __init__(self, index=0, size=200):
        super().__init__()

        self.name = "Form Generator"
        self.feature_names = ["email", "ip", "timestamp"]
        self.n_features = 0
        self.n_rows = size
        self._data = []
        self._data_index = index
        self.prepare_data()

    def next_sample(self, batch_size=1):
        self.n_features = len(self.feature_names)

        data = []

        for j in range(batch_size):
            arr = self._data[self._data_index]
            data.append(arr)
            self._data_index += 1

        return data

    def prepare_data(self):
        data = dict()
        data['email'] = self._faker('ascii_email', self.n_rows)
        data['ip'] = self._faker('ipv4', self.n_rows)
        data['timestamp'] = self._faker('unix_time', self.n_rows)

        for index in range(self.n_rows):
            arr = {}
            for name in self.feature_names:
                arr[name] = data[name][index]

            self._data.append(arr)

    def has_more_samples(self):
        if self._data_index >= self.n_rows:
            return False

        return True

    def _faker(self, type, size):
        fake = faker.Faker('en_US')
        arr = []
        for i in range(size):
            arr.append(getattr(fake, type)())

        return arr

    def _prepare_for_use(self):
        var = None
