import numpy as np
from abc import ABCMeta, abstractmethod
import warnings

__all__ = ['BaseEstimator', 'BaseSKMObject', 'SKStream', 'check_random_state']


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
