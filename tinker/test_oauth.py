#!.venv/bin/python -W ignore
import argparse

from bunq import ApiEnvironmentType
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.exception.bunq_exception import BunqException
from bunq.sdk.model.core.oauth_access_token import OauthAccessToken
from bunq.sdk.model.core.oauth_grant_type import OauthGrantType
from bunq.sdk.model.generated.endpoint import OauthClient

import user_overview
from libs.share_lib import ShareLib

# Option constants.
OPTION_AUTH_CODE = '--code'
OPTION_CONFIGURATION = '--configuration'
OPTION_REDIRECT_URI = '--redirect'

# API constants.
API_DEVICE_DESCRIPTION = "##### YOUR DEVICE DESCRIPTION #####"

# File constants.
FILE_OAUTH_CONFIGURATION = 'oauth.conf'
FILE_MODE_WRITE = 'w'
FILE_MODE_READ = 'r'

# Error constants.
ERROR_OPTION_MISSING_CODE = 'Missing mandatory option "--code [OAuth Authorisation Code]"'
ERROR_OPTION_MISSING_CONFIGURATION = 'Missing mandatory option "--configuration [OAuth Client file path]"'
ERROR_OPTION_MISSING_REDIRECT = 'Missing mandatory option "--redirect [redirect URI]"'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(OPTION_AUTH_CODE)
    parser.add_argument(OPTION_CONFIGURATION)
    parser.add_argument(OPTION_REDIRECT_URI)
    all_option = parser.parse_args()

    if all_option.code is None:
        raise BunqException(ERROR_OPTION_MISSING_CODE)

    if all_option.configuration is None:
        raise BunqException(ERROR_OPTION_MISSING_CONFIGURATION)

    if all_option.redirect is None:
        raise BunqException(ERROR_OPTION_MISSING_REDIRECT)

    BunqContext.load_api_context(ApiContext.restore(all_option.context))

    oauth_access_token = OauthAccessToken.create(
        OauthGrantType(OauthGrantType.AUTHORIZATION_CODE),
        all_option.code,
        all_option.redirect,
        create_oauth_client_from_file(all_option.configuration)
    )

    api_context = create_api_context_by_oauth_token(
        oauth_access_token,
        ShareLib.determine_environment_type_from_all_option(all_option)
    )

    BunqContext.load_api_context(api_context)

    user_overview.main()


def create_oauth_client_from_file(path: str) -> OauthClient:
    with open(path, FILE_MODE_READ) as file_:
        return OauthClient.from_json(file_.read())


def create_api_context_by_oauth_token(token: OauthAccessToken, api_environment_type: ApiEnvironmentType):
    return ApiContext.create(
        api_environment_type,
        token.token,
        API_DEVICE_DESCRIPTION
    )


if __name__ == '__main__':
    main()
