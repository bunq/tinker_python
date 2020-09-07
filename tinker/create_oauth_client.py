#!.venv/bin/python -W ignore
import os

from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.exception.bunq_exception import BunqException
from bunq.sdk.json import converter
from bunq.sdk.model.core.oauth_authorization_uri import OauthAuthorizationUri
from bunq.sdk.model.core.oauth_response_type import OauthResponseType
from bunq.sdk.model.generated.endpoint import OauthClient, OauthCallbackUrl

# File constants.
from libs.share_lib import ShareLib

FILE_OAUTH_CONFIGURATION = 'oauth.conf'
FILE_MODE_WRITE = 'w'
FILE_MODE_READ = 'r'

# Error constants.
ERROR_OPTION_MISSING_CONTEXT = 'Missing mandatory option "--context [API context]"'
ERROR_OPTION_MISSING_REDIRECT = 'Missing mandatory option "--redirect [redirect URI]"'


def main():
    all_option = ShareLib.parse_all_option()

    if all_option.context is None:
        raise BunqException(ERROR_OPTION_MISSING_CONTEXT)

    if all_option.redirect is None:
        raise BunqException(ERROR_OPTION_MISSING_REDIRECT)

    BunqContext.load_api_context(ApiContext.restore(all_option.context))

    if os.path.isfile(FILE_OAUTH_CONFIGURATION):
        oauth_client = create_oauth_client_from_file(FILE_OAUTH_CONFIGURATION)
    else:
        oauth_client_id = OauthClient.create().value
        OauthCallbackUrl.create(oauth_client_id, all_option.redirect)
        oauth_client = OauthClient.get(oauth_client_id).value

        serialized_client = converter.class_to_json(oauth_client)

        file = open(FILE_OAUTH_CONFIGURATION, FILE_MODE_WRITE)
        file.write(serialized_client)
        file.close()

    authorization_uri = OauthAuthorizationUri.create(
        OauthResponseType(OauthResponseType.CODE),
        all_option.redirect,
        oauth_client
    )
    ShareLib.print_header()

    print(f'''
      | Created OAuth client!
      | Point your user to the following URL to obtain an auth code:
      | {authorization_uri.get_authorization_uri()}
    ''')


def create_oauth_client_from_file(path: str) -> OauthClient:
    with open(path, FILE_MODE_READ) as file_:
        return OauthClient.from_json(file_.read())


if __name__ == '__main__':
    main()
