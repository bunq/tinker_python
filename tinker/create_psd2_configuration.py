#!.venv/bin/python -W ignore
import argparse

from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.exception.bunq_exception import BunqException

from libs.share_lib import ShareLib

# API constants.
API_DEVICE_DESCRIPTION = "##### YOUR DEVICE DESCRIPTION #####"

# File constants.
FILE_OAUTH_CONFIGURATION = 'oauth.conf'
FILE_MODE_WRITE = 'w'
FILE_MODE_READ = 'r'

# Option constants.
OPTION_CERTIFICATE = "--certificate"
OPTION_CERTIFICATE_CHAIN = "--chain"
OPTION_PRIVATE_KEY = "--key"

# Error constants.
ERROR_OPTION_MISSING_CERTIFICATE = 'Missing mandatory option "--certificate [certificate]"'
ERROR_OPTION_MISSING_CERTIFICATE_CHAIN = 'Missing mandatory option "--chain [certificate chain]"'
ERROR_OPTION_MISSING_PRIVATE_KEY = 'Missing mandatory option "--key [private key]"'

# File constants.
FILE_CONTEXT = "bunq-psd2.conf"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(OPTION_CERTIFICATE)
    parser.add_argument(OPTION_CERTIFICATE_CHAIN)
    parser.add_argument(OPTION_PRIVATE_KEY)
    all_option = parser.parse_args()

    if all_option.certificate is None:
        raise BunqException(ERROR_OPTION_MISSING_CERTIFICATE)

    if all_option.chain is None:
        raise BunqException(ERROR_OPTION_MISSING_CERTIFICATE_CHAIN)

    if all_option.key is None:
        raise BunqException(ERROR_OPTION_MISSING_PRIVATE_KEY)

    api_context = ApiContext.create_for_psd2(
        ShareLib.determine_environment_type_from_all_option(all_option),
        get_from_file(all_option.certificate),
        get_from_file(all_option.key),
        [get_from_file(all_option.chain)],
        API_DEVICE_DESCRIPTION,
        []
    )

    api_context.save(FILE_CONTEXT)

    ShareLib.print_header()

    print(f'''
      | PSD2 configuration created. Saved as bunq-psd2.conf!
    ''')


def get_from_file(path: str) -> str:
    with open(path, FILE_MODE_READ) as file_:
        return file_.read()


if __name__ == '__main__':
    main()
