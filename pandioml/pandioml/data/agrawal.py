from pandioml.data.stream import Stream
from pandioml.data.record import Record, Float, Integer
from skmultiflow.data import AGRAWALGenerator


class AgrawalGenerator(Stream):
    """
    A generator for data regarding home loan applications with the ability to balance and add noise.

    Each record is an instance of LoanApplication

    class LoanApplication(Record):
        salary = Float()
        commission = Float()
        age = Float()
        education_level = Integer()
        car = Float()
        zipcode = Float()
        house_value = Float()
        house_owned_years = Integer()
        loan_amount = Float()
        label = Integer()
    """

    generator = None

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.generator = AGRAWALGenerator(*args, **kwargs)

    def next(self):
        features, label = self.generator.next_sample()

        dict = {'label': label[0].item()}

        index = 0
        for element in features[0]:
            dict[self.generator.feature_names[index]] = element.item()
            index += 1

        return LoanApplication(**dict)


class LoanApplication(Record):
    salary = Float()
    commission = Float()
    age = Float()
    education_level = Integer()
    car = Float()
    zipcode = Float()
    house_value = Float()
    house_owned_years = Integer()
    loan_amount = Float()
    label = Integer()
