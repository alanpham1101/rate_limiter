from algorithms import (
    TokenBucket,
    LeakyBucket,
)


class RateLimiterAlgorithm:
    TOKEN_BUCKET = 'token_bucket'
    LEAKY_BUCKET = 'leaky_bucket'


class ErrorMessage:
    INVALID_OPTION = "Wrong running option."
    UNPROCESSABLE_OPTION = "Cannot process running option."
    MISSING_ENV_PARAMS = "Missing environment parameters."
    GENERAL = "Something went wrongs."


RATE_LIMITER_ALGO_MAPPING = (
    (RateLimiterAlgorithm.TOKEN_BUCKET, TokenBucket),
    (RateLimiterAlgorithm.LEAKY_BUCKET, LeakyBucket),
)
