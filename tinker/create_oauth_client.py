#!.venv/bin/python -W ignore
import argparse
import os

from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.exception.bunq_exception import BunqException
from bunq.sdk.json import converter
from bunq.sdk.model.generated.endpoint import OauthClient, OauthCallbackUrl

# File constants.
FILE_OAUTH_CONFIGURATION = 'oauth.conf'
FILE_MODE_WRITE = 'w'

# Option constants.
OPTION_CONTEXT = '--context'
OPTION_REDIRECT_URI = '--redirect'

# Error constants.
ERROR_OPTION_MISSING_CONTEXT = 'Missing mandatory option "--context [API context]"'
ERROR_OPTION_MISSING_REDIRECT = 'Missing mandatory option "--redirect [redirect URI]"'


# TODO: ALL_OAUTH_CONFIGURATION_OPTION


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(OPTION_CONTEXT)
    parser.add_argument(OPTION_REDIRECT_URI)
    all_option = parser.parse_args()

    if all_option.context is None:
        raise BunqException(ERROR_OPTION_MISSING_CONTEXT)

    if all_option.redirect is None:
        raise BunqException(ERROR_OPTION_MISSING_REDIRECT)

    BunqContext.load_api_context(ApiContext.restore(all_option.context))

    if os.path.isfile(FILE_OAUTH_CONFIGURATION):
        oauth_client = None  # TODO: Create Oauth Client from file.
    else:
        oauth_client_id = OauthClient.create().value
        OauthCallbackUrl.create(oauth_client_id, all_option.redirect)
        oauth_client = OauthClient.get(oauth_client_id).value

        serialized_client = converter.class_to_json(oauth_client)

        file = open(FILE_OAUTH_CONFIGURATION, FILE_MODE_WRITE)
        file.write(serialized_client)
        file.close()

    # authorization_uri = OauthAuthorizationUri
    # ShareLib.print_header()
    #
    # print(f'''
    #   | Checking for ApiContext file.
    #
    #     ...
    # ''')


if __name__ == '__main__':
    main()
