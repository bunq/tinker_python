#!.venv/bin/python -W ignore
import argparse
import socket

from bunq.sdk.context import ApiContext
from bunq.sdk.context import ApiEnvironmentType
from bunq.sdk.exception import BunqException

# Option constants.
OPTION_API_KEY = '--api-key'

# Error constants.
ERROR_OPTION_MISSING_API_KEY = 'Missing mandatory option "--api-key [API key]"'

# Configuration file name constant.
DEFAULT_BUNQ_CONFIGURATION_FILE_NAME_PRODUCTION = 'bunq-production.conf'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(OPTION_API_KEY)
    all_option = parser.parse_args()

    if all_option.api_key is None:
        raise BunqException(ERROR_OPTION_MISSING_API_KEY)

    api_context = ApiContext(ApiEnvironmentType.PRODUCTION, all_option.api_key, socket.gethostname())
    api_context.save(DEFAULT_BUNQ_CONFIGURATION_FILE_NAME_PRODUCTION)


if __name__ == '__main__':
    main()
