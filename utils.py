import os

from constants import (
    RATE_LIMITER_ALGO_MAPPING,
    RateLimiterAlgorithm,
    ErrorMessage
)
from exceptions import (
    InvalidOption,
    UnprocesableOption,
    MissingEnvironmentParameters,
)


def error_handing(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidOption:
            print(ErrorMessage.INVALID_OPTION)
        except UnprocesableOption:
            print(ErrorMessage.UNPROCESSABLE_OPTION)
        except MissingEnvironmentParameters:
            print(ErrorMessage.MISSING_ENV_PARAMS)
        except Exception as e:
            print(f"{ErrorMessage.GENERAL}\nError: {str(e)}")
    return inner_function


@error_handing
def get_rate_limiter_obj(option):
    option_mapping = dict(RATE_LIMITER_ALGO_MAPPING)
    if option not in option_mapping:
        raise InvalidOption

    parameters = get_parameters(option)
    rate_limiter = option_mapping[option]
    return rate_limiter(*parameters)


@error_handing
def get_parameters(option):
    try:
        if option == RateLimiterAlgorithm.TOKEN_BUCKET:
            bucket_capacity = os.getenv("TOKEN_BUCKET_CAPACITY")
            bucket_refill_rate = os.getenv("TOKEN_BUCKET_REFILL_RATE")
            return int(bucket_capacity), int(bucket_refill_rate)
        elif option == RateLimiterAlgorithm.LEAKY_BUCKET:
            bucket_capacity = os.getenv("LEAKY_BUCKET_CAPACITY")
            bucket_outflow_rate = os.getenv("LEAKY_BUCKET_OUTFLOW_RATE")
            return int(bucket_capacity), int(bucket_outflow_rate)
        else:
            raise UnprocesableOption
    except Exception:
        raise MissingEnvironmentParameters
