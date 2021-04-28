from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, Float, Integer
from abc import ABCMeta, abstractmethod
import warnings
import numpy as np


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
        self.generator = AGRAWAL(*args, **kwargs)

    def next(self):
        features, label = self.generator.next_sample()

        dict = {'label': label[0].item()}

        index = 0
        for element in features[0]:
            dict[self.generator.feature_names[index]] = element.item()
            index += 1

        return LoanApplication(**dict)

    @staticmethod
    def schema():
        return JsonSchema(LoanApplication)


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


""" Below classes taken from scikit-multiflow python library, now deprecated """


class BaseEstimator:
    """Base Estimator class for compatibility with scikit-learn.

    Notes
    -----
    * All estimators should specify all the parameters that can be set
      at the class level in their ``__init__`` as explicit keyword
      arguments (no ``*args`` or ``**kwargs``).
    * Taken from sklearn for compatibility.
    """

    @classmethod
    def _get_param_names(cls):
        """Get parameter names for the estimator"""
        # fetch the constructor or the original constructor before
        # deprecation wrapping if any
        init = getattr(cls.__init__, 'deprecated_original', cls.__init__)
        if init is object.__init__:
            # No explicit constructor to introspect
            return []

        # introspect the constructor arguments to find the model parameters
        # to represent
        init_signature = inspect.signature(init)
        # Consider the constructor parameters excluding 'self'
        parameters = [p for p in init_signature.parameters.values()
                      if p.name != 'self' and p.kind != p.VAR_KEYWORD]
        for p in parameters:
            if p.kind == p.VAR_POSITIONAL:
                raise RuntimeError("scikit-multiflow estimators should always "
                                   "specify their parameters in the signature"
                                   " of their __init__ (no varargs)."
                                   " %s with constructor %s doesn't "
                                   " follow this convention."
                                   % (cls, init_signature))
        # Extract and sort argument names excluding 'self'
        return sorted([p.name for p in parameters])

    def get_params(self, deep=True):
        """Get parameters for this estimator.

        Parameters
        ----------
        deep : boolean, optional
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        out = dict()
        for key in self._get_param_names():
            value = getattr(self, key, None)
            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '__' + k, val) for k, val in deep_items)
            out[key] = value
        return out

    def set_params(self, **params):
        """Set the parameters of this estimator.

        The method works on simple estimators as well as on nested objects
        (such as pipelines). The latter have parameters of the form
        ``<component>__<parameter>`` so that it's possible to update each
        component of a nested object.

        Returns
        -------
        self
        """
        if not params:
            # Simple optimization to gain speed (inspect is slow)
            return self
        valid_params = self.get_params(deep=True)

        nested_params = defaultdict(dict)  # grouped by prefix
        for key, value in params.items():
            key, delim, sub_key = key.partition('__')
            if key not in valid_params:
                raise ValueError('Invalid parameter %s for estimator %s. '
                                 'Check the list of available parameters '
                                 'with `estimator.get_params().keys()`.' %
                                 (key, self))

            if delim:
                nested_params[key][sub_key] = value
            else:
                setattr(self, key, value)
                valid_params[key] = value

        for key, sub_params in nested_params.items():
            valid_params[key].set_params(**sub_params)

        return self

    def __repr__(self, N_CHAR_MAX=700):
        # N_CHAR_MAX is the (approximate) maximum number of non-blank
        # characters to render. We pass it as an optional parameter to ease
        # the tests.

        from ..utils._pprint import _EstimatorPrettyPrinter

        N_MAX_ELEMENTS_TO_SHOW = 30  # number of elements to show in sequences

        # use ellipsis for sequences with a lot of elements
        pp = _EstimatorPrettyPrinter(
            compact=True, indent=1, indent_at_name=True,
            n_max_elements_to_show=N_MAX_ELEMENTS_TO_SHOW)

        repr_ = pp.pformat(self)

        # Use bruteforce ellipsis when there are a lot of non-blank characters
        n_nonblank = len(''.join(repr_.split()))
        if n_nonblank > N_CHAR_MAX:
            lim = N_CHAR_MAX // 2  # apprx number of chars to keep on both ends
            regex = r'^(\s*\S){%d}' % lim
            # The regex '^(\s*\S){%d}' % n
            # matches from the start of the string until the nth non-blank
            # character:
            # - ^ matches the start of string
            # - (pattern){n} matches n repetitions of pattern
            # - \s*\S matches a non-blank char following zero or more blanks
            left_lim = re.match(regex, repr_).end()
            right_lim = re.match(regex, repr_[::-1]).end()

            if '\n' in repr_[left_lim:-right_lim]:
                # The left side and right side aren't on the same line.
                # To avoid weird cuts, e.g.:
                # categoric...ore',
                # we need to start the right side with an appropriate newline
                # character so that it renders properly as:
                # categoric...
                # handle_unknown='ignore',
                # so we add [^\n]*\n which matches until the next \n
                regex += r'[^\n]*\n'
                right_lim = re.match(regex, repr_[::-1]).end()

            ellipsis = '...'
            if left_lim + len(ellipsis) < len(repr_) - right_lim:
                # Only add ellipsis if it results in a shorter repr
                repr_ = repr_[:left_lim] + '...' + repr_[-right_lim:]

        return repr_

    def __getstate__(self):
        try:
            state = super().__getstate__()
        except AttributeError:
            state = self.__dict__.copy()

        if type(self).__module__.startswith('skmultiflow.'):
            return dict(state.items(), _skmultiflow_version=__version__)
        else:
            return state

    def __setstate__(self, state):
        if type(self).__module__.startswith('skmultiflow.'):
            pickle_version = state.pop("_skmultiflow_version", "pre-0.18")
            if pickle_version != __version__:
                warnings.warn(
                    "Trying to unpickle estimator {0} from version {1} when "
                    "using version {2}. This might lead to breaking code or "
                    "invalid results. Use at your own risk.".format(
                        self.__class__.__name__, pickle_version, __version__),
                    UserWarning)
        try:
            super().__setstate__(state)
        except AttributeError:
            self.__dict__.update(state)

    def _get_tags(self):
        collected_tags = {}
        for base_class in inspect.getmro(self.__class__):
            if (hasattr(base_class, '_more_tags') and base_class != self.__class__):
                more_tags = base_class._more_tags(self)
                collected_tags = _update_if_consistent(collected_tags,
                                                       more_tags)
        if hasattr(self, '_more_tags'):
            more_tags = self._more_tags()
            collected_tags = _update_if_consistent(collected_tags, more_tags)
        tags = _DEFAULT_TAGS.copy()
        tags.update(collected_tags)
        return tags


class BaseSKMObject(BaseEstimator):
    """Base class for most objects in scikit-multiflow

        Notes
        -----
        This class provides additional functionality not available in the base estimator
        from scikit-learn
    """
    def reset(self):
        """ Resets the estimator to its initial state.

        Returns
        -------
        self

        """
        # non-optimized default implementation; override if a better
        # method is possible for a given object
        command = ''.join([line.strip() for line in self.__repr__().split()])
        command = command.replace(str(self.__class__.__name__), 'self.__init__')
        exec(command)

    def get_info(self):
        """ Collects and returns the information about the configuration of the estimator

        Returns
        -------
        string
            Configuration of the estimator.
        """
        return self.__repr__()


class SKStream(BaseSKMObject, metaclass=ABCMeta):
    """ Base Stream class.

    This abstract class defines the minimum requirements of a stream,
    so that it can work along other modules in scikit-multiflow.

    Raises
    ------
    NotImplementedError: This is an abstract class.

    """
    _estimator_type = 'stream'

    def __init__(self):
        self.n_samples = 0
        self.n_targets = 0
        self.n_features = 0
        self.n_num_features = 0
        self.n_cat_features = 0
        self.n_classes = 0
        self.cat_features_idx = []
        self.current_sample_x = None
        self.current_sample_y = None
        self.sample_idx = 0
        self.feature_names = None
        self.target_names = None
        self.target_values = None
        self.name = None

    @property
    def n_features(self):
        """ Retrieve the number of features.

        Returns
        -------
        int
            The total number of features.

        """
        return self._n_features

    @n_features.setter
    def n_features(self, n_features):
        """ Set the number of features

        """
        self._n_features = n_features

    @property
    def n_cat_features(self):
        """ Retrieve the number of integer features.

        Returns
        -------
        int
            The number of integer features in the stream.

        """
        return self._n_cat_features

    @n_cat_features.setter
    def n_cat_features(self, n_cat_features):
        """ Set the number of integer features

        Parameters
        ----------
        n_cat_features: int
        """
        self._n_cat_features = n_cat_features

    @property
    def n_num_features(self):
        """ Retrieve the number of numerical features.

        Returns
        -------
        int
            The number of numerical features in the stream.

        """
        return self._n_num_features

    @n_num_features.setter
    def n_num_features(self, n_num_features):
        """ Set the number of numerical features

        Parameters
        ----------
        n_num_features: int

        """
        self._n_num_features = n_num_features

    @property
    def n_targets(self):
        """ Retrieve the number of targets

        Returns
        -------
        int
            the number of targets in the stream.
        """
        return self._target_idx

    @n_targets.setter
    def n_targets(self, n_targets):
        """ Set the number of targets

        Parameters
        ----------
        n_targets: int
        """
        self._target_idx = n_targets

    @property
    def target_values(self):
        """ Retrieve all target_values in the stream for each target.

        Returns
        -------
        list
            list of lists of all target_values for each target
        """
        return self._target_values

    @target_values.setter
    def target_values(self, target_values):
        """ Set the list for all target_values in the stream.

        Parameters
        ----------
        target_values
        """
        self._target_values = target_values

    @property
    def feature_names(self):
        """ Retrieve the names of the features.

        Returns
        -------
        list
            names of the features
        """
        return self._feature_names

    @feature_names.setter
    def feature_names(self, feature_names):
        """ Set the name of the features in the stream.

        Parameters
        ----------
        feature_names: list
        """
        self._feature_names = feature_names

    @property
    def target_names(self):
        """ Retrieve the names of the targets

        Returns
        -------
        list
            the names of the targets in the stream.
        """
        return self._target_names

    @target_names.setter
    def target_names(self, target_names):
        """ Set the names of the targets in the stream.

        Parameters
        ----------
        target_names: list

        """
        self._target_names = target_names

    @staticmethod
    def prepare_for_use():  # pragma: no cover
        """ Prepare the stream for use.

        Deprecated in v0.5.0 and will be removed in v0.7.0

        """
        warnings.warn(
            "'prepare_for_use' has been deprecated in v0.5.0 and will be removed in v0.7.0.\n"
            "New instances of the Stream class are now ready to use after instantiation.",
            category=FutureWarning)

    @abstractmethod
    def _prepare_for_use(self):
        raise NotImplementedError

    @abstractmethod
    def next_sample(self, batch_size=1):
        """ Returns next sample from the stream.

        Parameters
        ----------
        batch_size: int (optional, default=1)
            The number of samples to return.

        Returns
        -------
        tuple or tuple list
            A numpy.ndarray of shape (batch_size, n_features) and an array-like of size
            n_targets, representing the next batch_size samples.

        """
        raise NotImplementedError

    def last_sample(self):
        """ Retrieves last `batch_size` samples in the stream.

        Returns
        -------
        tuple or tuple list
            A numpy.ndarray of shape (batch_size, n_features) and an array-like of shape
            (batch_size, n_targets), representing the next batch_size samples.

        """
        return self.current_sample_x, self.current_sample_y

    def is_restartable(self):
        """
        Determine if the stream is restartable.

        Returns
        -------
        Bool
            True if stream is restartable.

        """
        return True

    def restart(self):
        """  Restart the stream. """
        self.current_sample_x = None
        self.current_sample_y = None
        self.sample_idx = 0
        self._prepare_for_use()

    def n_remaining_samples(self):
        """ Returns the estimated number of remaining samples.

        Returns
        -------
        int
            Remaining number of samples. -1 if infinite (e.g. generator)

        """
        return -1

    def has_more_samples(self):
        """
        Checks if stream has more samples.

        Returns
        -------
        Boolean
            True if stream has more samples.
        """
        return True

    def get_data_info(self):
        """ Retrieves minimum information from the stream

        Used by evaluator methods to id the stream.

        The default format is: 'Stream name - n_targets, n_classes, n_features'.

        Returns
        -------
        string
            Stream data information

        """
        return self.name + " - {} target(s), {} classes, {} features".format(self.n_targets,
                                                                             self.n_classes,
                                                                             self.n_features)


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance.

    Parameters
    ----------
    seed : None | int | instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.

    Notes
    -----
    Code from sklearn

    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('{} cannot be used to seed a numpy.random.RandomState instance'.format(seed))


class AGRAWAL(SKStream):
    """ Agrawal stream generator.

    The generator was introduced by Agrawal et al. in [1]_, and was common source
    of data for early work on scaling up decision tree learners.
    The generator produces a stream containing nine features, six numeric and
    three categorical.
    There are ten functions defined for generating binary class labels from the
    features. Presumably these determine whether the loan should be approved.
    The features and functions are listed in the original paper [1]_.

    .. list-table::
       :widths: 25 25 50
       :header-rows: 1

       * - feature name
         - feature description
         - values
       * - salary
         - the salary
         - uniformly distributed from 20k to 150k
       * - commission
         - the commission
         - if (salary < 75k) then 0 else uniformly distributed from 10k to 75k
       * - age
         - the age
         - uniformly distributed from 20 to 80
       * - elevel
         - the education level
         - uniformly chosen from 0 to 4
       * - car
         - car maker
         - uniformly chosen from 1 to 20
       * - zipcode
         - zip code of the town
         - uniformly chosen from 0 to 8
       * - hvalue
         - value of the house
         - uniformly distributed from 50k x zipcode to 100k x zipcode
       * - hyears
         - years house owned
         - uniformly distributed from 1 to 30
       * - loan
         - total loan amount
         - uniformly distributed from 0 to 500k

    Parameters
    ----------
    classification_function: int (Default=0)
        Which of the four classification functions to use for the generation.
        The value can vary from 0 to 9.

    random_state: int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    balance_classes: bool (Default: False)
        Whether to balance classes or not. If balanced, the class
        distribution will converge to a uniform distribution.

    perturbation: float (Default: 0.0)
        The probability that noise will happen in the generation. At each
        new sample generated, the sample with will perturbed by the amount of
        perturbation.
        Values go from 0.0 to 1.0.

    References
    ----------
    .. [1] Rakesh Agrawal, Tomasz Imielinksi, and Arun Swami. "Database
       Mining: A Performance Perspective", IEEE Transactions on Knowledge and
       Data Engineering, 5(6), December 1993.

    """

    def __init__(self, classification_function=0, random_state=None, balance_classes=False,
                 perturbation=0.0):
        super().__init__()

        # Classification functions to use
        self._classification_functions = [self._classification_function_zero,
                                          self._classification_function_one,
                                          self._classification_function_two,
                                          self._classification_function_three,
                                          self._classification_function_four,
                                          self._classification_function_five,
                                          self._classification_function_six,
                                          self._classification_function_seven,
                                          self._classification_function_eight,
                                          self._classification_function_nine]
        self.classification_function = classification_function
        self.random_state = random_state
        self.balance_classes = balance_classes
        self.perturbation = perturbation
        self.n_num_features = 6
        self.n_cat_features = 3
        self.n_features = self.n_num_features + self.n_cat_features
        self.n_classes = 2
        self.n_targets = 1
        self._random_state = None  # This is the actual random_state object used internally
        self._next_class_should_be_zero = False
        self.name = "AGRAWAL Generator"

        self.target_names = ["target"]
        self.feature_names = ["salary", "commission", "age", "elevel", "car", "zipcode", "hvalue",
                              "hyears", "loan"]
        self.target_values = [i for i in range(self.n_classes)]

        self._prepare_for_use()

    @property
    def classification_function(self):
        """ Retrieve the index of the current classification function.

        Returns
        -------
        int
            index of the classification function, from 0 to 9
        """
        return self._classification_function

    @classification_function.setter
    def classification_function(self, classification_function_idx):
        """ Set the index of the current classification function.

        Parameters
        ----------
        classification_function_idx: int
            from 0 to 9
        """
        if classification_function_idx in range(10):
            self._classification_function = classification_function_idx
        else:
            raise ValueError("classification_function takes values from 0 to 9,"
                             " and {} was passed".format(classification_function_idx))

    @property
    def balance_classes(self):
        """ Retrieve the value of the option: Balance classes

        Returns
        -------
        Boolean
            True is the classes are balanced
        """
        return self._balance_classes

    @balance_classes.setter
    def balance_classes(self, balance_classes):
        """ Set the value of the option: Balance classes.

        Parameters
        ----------
        balance_classes: Boolean

        """
        if isinstance(balance_classes, bool):
            self._balance_classes = balance_classes
        else:
            raise ValueError(
                "balance_classes should be boolean, and {} was passed".format(balance_classes))

    @property
    def perturbation(self):
        """ Retrieve the value of the option: Noise percentage

        Returns
        -------
        float

        """
        return self._perturbation

    @perturbation.setter
    def perturbation(self, perturbation):
        """ Set the value of the option: Perturbation.

        Parameters
        ----------
        perturbation: float
            from 0.0 to 1.0.

        """
        if (0.0 <= perturbation) and (perturbation <= 1.0):
            self._perturbation = perturbation
        else:
            raise ValueError(
                "noise percentage should be in [0.0..1.0], and {} was passed".format(perturbation))

    def _prepare_for_use(self):
        self._random_state = check_random_state(self.random_state)
        self._next_class_should_be_zero = False

    def next_sample(self, batch_size=1):
        """ Returns next sample from the stream.

        The sample generation works as follows: The 9 features are generated
        with the random generator, initialized with the seed passed by the
        user. Then, the classification function decides, as a function of all
        the attributes, whether to classify the instance as class 0 or class
        1. The next step is to verify if the classes should be balanced, and
        if so, balance the classes. The last step is to add noise, if the noise
        percentage is higher than 0.0.

        The generated sample will have 9 features and 1 label (it has one
        classification task).

        Parameters
        ----------
        batch_size: int (optional, default=1)
            The number of samples to return.

        Returns
        -------
        tuple or tuple list
            Return a tuple with the features matrix and the labels matrix for
            the batch_size samples that were requested.

        """
        data = np.zeros([batch_size, self.n_features + 1])

        for j in range(batch_size):
            self.sample_idx += 1
            group = 0
            desired_class_found = False
            while not desired_class_found:
                salary = 20000 + 130000 * self._random_state.rand()
                commission = 0 if (salary >= 75000) else (
                    10000 + 75000 * self._random_state.rand())
                age = 20 + self._random_state.randint(61)
                elevel = self._random_state.randint(5)
                car = self._random_state.randint(20)
                zipcode = self._random_state.randint(9)
                hvalue = (9 - zipcode) * 100000 * (0.5 + self._random_state.rand())
                hyears = 1 + self._random_state.randint(30)
                loan = self._random_state.rand() * 500000
                group = self._classification_functions[self.classification_function](salary,
                                                                                     commission,
                                                                                     age, elevel,
                                                                                     car,
                                                                                     zipcode,
                                                                                     hvalue,
                                                                                     hyears, loan)
                if not self.balance_classes:
                    desired_class_found = True
                else:
                    if (self._next_class_should_be_zero and (group == 0)) or \
                            ((not self._next_class_should_be_zero) and (group == 1)):
                        desired_class_found = True
                        self._next_class_should_be_zero = not self._next_class_should_be_zero

            if self.perturbation > 0.0:
                salary = self._perturb_value(salary, 20000, 150000)
                if commission > 0:
                    commission = self._perturb_value(commission, 10000, 75000)
                age = np.round(self._perturb_value(age, 20, 80))
                hvalue = self._perturb_value(hvalue, (9 - zipcode) * 100000, 0, 135000)
                hyears = np.round(self._perturb_value(hyears, 1, 30))
                loan = self._perturb_value(loan, 0, 500000)

            for i in range(9):
                data[j, i] = eval(self.feature_names[i])
            data[j, 9] = group

        self.current_sample_x = data[:, :self.n_features]
        self.current_sample_y = data[:, self.n_features:].flatten().astype(int)

        return self.current_sample_x, self.current_sample_y

    def _perturb_value(self, val, val_min, val_max, val_range=None):
        """
        Perturbs the values of the features by adding noise after assigning a label,
        if the perturbation is higher than 0.0.

        Parameters
        ----------
        val: float
            The value to add noise to.
        val_min: float
            The minimum value after perturbation.
        val_max: float
            The maximum value after perturbation.
        val_range:
            The range of the perturbation.

        Returns
        -------
        float
            The value after perturbation.
        """
        if val_range is None:
            val_range = val_max - val_min
        val += val_range * (2 * (self._random_state.rand() - 0.5)) * self.perturbation
        if val < val_min:
            val = val_min
        elif val > val_max:
            val = val_max
        return val

    def generate_drift(self):
        """
        Generate drift by switching the classification function randomly.

        """
        new_function = self._random_state.randint(10)
        while new_function == self.classification_function:
            new_function = self._random_state.randint(10)
        self.classification_function = new_function

    @staticmethod
    def _classification_function_zero(salary, commission, age, elevel, car, zipcode, hvalue,
                                      hyears, loan):
        """ classification_function_zero

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """

        return 0 if ((age < 40) or (60 <= age)) else 1

    @staticmethod
    def _classification_function_one(salary, commission, age, elevel, car, zipcode, hvalue, hyears,
                                     loan):
        """ classification_function_one

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """

        if age < 40:
            return 0 if ((50000 <= salary) and (salary <= 100000)) else 1
        elif age < 60:
            return 0 if ((75000 <= salary) and (salary <= 125000)) else 1
        else:
            return 0 if ((25000 <= salary) and (salary <= 75000)) else 1

    @staticmethod
    def _classification_function_two(salary, commission, age, elevel, car, zipcode, hvalue, hyears,
                                     loan):
        """ classification_function_two

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """

        if age < 40:
            return 0 if ((elevel == 0) or (elevel == 1)) else 1
        elif age < 60:
            return 0 if ((elevel == 1) or (elevel == 2) or (elevel == 3)) else 1
        else:
            return 0 if ((elevel == 2) or (elevel == 3)) or (elevel == 4) else 1

    @staticmethod
    def _classification_function_three(salary, commission, age, elevel, car, zipcode, hvalue,
                                       hyears, loan):
        """ classification_function_three

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """

        if age < 40:
            if (elevel == 0) or (elevel == 1):
                return 0 if ((25000 <= salary) and (salary <= 75000)) else 1
            else:
                return 0 if ((50000 <= salary) and (salary <= 100000)) else 1
        elif age < 60:
            if (elevel == 1) or (elevel == 2) or (elevel == 3):
                return 0 if ((50000 <= salary) and (salary <= 100000)) else 1
            else:
                return 0 if ((75000 <= salary) and (salary <= 125000)) else 1
        else:
            if (elevel == 2) or (elevel == 3) or (elevel == 4):
                return 0 if ((50000 <= salary) and (salary <= 100000)) else 1
            else:
                return 0 if ((25000 <= salary) and (salary <= 75000)) else 1

    @staticmethod
    def _classification_function_four(salary, commission, age, elevel, car, zipcode, hvalue,
                                      hyears, loan):
        """ classification_function_four

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """

        if age < 40:
            if (50000 <= salary) and (salary <= 100000):
                return 0 if ((100000 <= loan) and (loan <= 300000)) else 1
            else:
                return 0 if ((200000 <= salary) and (salary <= 400000)) else 1
        elif age < 60:
            if (75000 <= salary) and (salary <= 125000):
                return 0 if ((200000 <= salary) and (loan <= 400000)) else 1
            else:
                return 0 if ((300000 <= salary) and (salary <= 500000)) else 1
        else:
            if (25000 <= salary) and (salary <= 75000):
                return 0 if ((300000 <= loan) and (loan <= 500000)) else 1
            else:
                return 0 if ((75000 <= loan) and (loan <= 300000)) else 1

    @staticmethod
    def _classification_function_five(salary, commission, age, elevel, car, zipcode, hvalue,
                                      hyears, loan):
        """ classification_function_five

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """

        totalsalary = salary + commission

        if age < 40:
            return 0 if ((50000 <= totalsalary) and (totalsalary <= 100000)) else 1
        elif age < 60:
            return 0 if ((75000 <= totalsalary) and (totalsalary <= 125000)) else 1
        else:
            return 0 if ((25000 <= totalsalary) and (totalsalary <= 75000)) else 1

    @staticmethod
    def _classification_function_six(salary, commission, age, elevel, car, zipcode, hvalue, hyears,
                                     loan):
        """ classification_function_six

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """
        disposable = (2 * (salary + commission) / 3 - loan / 5 - 20000)
        return 0 if disposable > 1 else 1

    @staticmethod
    def _classification_function_seven(salary, commission, age, elevel, car, zipcode, hvalue,
                                       hyears, loan):
        """ classification_function_seven

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """
        disposable = (2 * (salary + commission) / 3 - 5000 * elevel - 20000)
        return 0 if disposable > 1 else 1

    @staticmethod
    def _classification_function_eight(salary, commission, age, elevel, car, zipcode, hvalue,
                                       hyears, loan):
        """ classification_function_eight

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """
        disposable = (2 * (salary + commission) / 3 - 5000 * elevel - loan / 5 - 10000)
        return 0 if disposable > 1 else 1

    @staticmethod
    def _classification_function_nine(salary, commission, age, elevel, car, zipcode, hvalue,
                                      hyears, loan):
        """ classification_function_nine

        Parameters
        ----------
        salary: float
            Numeric feature: Salary.

        commission: float
            Numeric feature: Commission.

        age: int
            Numeric feature: Age.

        elevel: int
            Categorical feature: Education level.

        car: int
            Categorical feature: Car maker.

        zipcode; int
            Categorical feature: Zipcode.

        hvalue: flaot
            Numeric feature: Value of the house.

        hyears: float
            Numeric feature: Years house owned.

        loan: float
            Numeric feature: Total amount of loan.

        Returns
        -------
        int
            Returns the sample class label, either 0 or 1.

        """
        equity = 0
        if hyears >= 20:
            equity = hvalue * (hyears - 20) / 10
        disposable = (2 * (salary + commission) / 3 - 5000 * elevel + equity / 5 - 10000)
        return 0 if disposable > 1 else 1
