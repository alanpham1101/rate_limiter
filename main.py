import sys
from dotenv import load_dotenv

from utils import get_rate_limiter_obj


def run_rate_limiter(option):
    obj = get_rate_limiter_obj(option)
    obj.handle()


if __name__ == "__main__":
    option = sys.argv[1]
    load_dotenv()
    run_rate_limiter(option)
