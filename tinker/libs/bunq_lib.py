import json
import socket
from os import remove
from os.path import isfile
from time import sleep
from typing import Union, List

import requests
from bunq import ApiEnvironmentType, Pagination
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.exception.bunq_exception import BunqException
from bunq.sdk.exception.forbidden_exception import ForbiddenException
from bunq.sdk.model.core.notification_filter_url_user_internal import NotificationFilterUrlUserInternal
from bunq.sdk.model.generated.endpoint import UserCompany, UserPerson, MonetaryAccountBank, UserLight, User, Payment, \
    RequestInquiry, Card, NotificationFilterUrlUser, SandboxUserPerson
from bunq.sdk.model.generated.object_ import Amount, NotificationFilterUrl
from bunq.sdk.model.generated.object_ import CardPinAssignment
from bunq.sdk.model.generated.object_ import Pointer

NOTIFICATION_DELIVERY_METHOD_URL = 'URL'

NOTIFICATION_CATEGORY_MUTATION = 'MUTATION'


class BunqLib(object):
    _ERROR_COULD_NOT_DETERMINE_CONF = 'Could not find the bunq configuration file.'
    _ERROR_COULD_NOT_CREATE_NEW_SANDBOX_USER = "Could not create new sandbox user."
    _BUNQ_CONF_PRODUCTION = 'bunq-production.conf'
    _BUNQ_CONF_SANDBOX = 'bunq-sandbox.conf'

    _MONETARY_ACCOUNT_STATUS_ACTIVE = 'ACTIVE'

    _CARD_PIN_ASSIGNMENT_TYPE = 'PRIMARY'

    _DEFAULT_COUNT = 10
    _POINTER_TYPE_EMAIL = 'EMAIL'
    _CURRENCY_EUR = 'EUR'
    _DEVICE_DESCRIPTION = "python tinker"

    _REQUEST_SPENDING_MONEY_AMOUNT = '500.0'
    _REQUEST_SPENDING_MONEY_RECIPIENT = 'sugardaddy@bunq.com'
    _REQUEST_SPENDING_MONEY_DESCRIPTION = 'Requesting some spending money.'
    _REQUEST_SPENDING_MONEY_WAIT_TIME_SECONDS = 1

    _ZERO_BALANCE = 0.0

    def __init__(self, env: ApiEnvironmentType):
        self.user = None
        self.env = env
        self.setup_context()
        self.setup_current_user()
        self.__request_spending_money_if_needed()

    def setup_context(self, reset_config_if_needed=True):
        if isfile(self.determine_bunq_conf_filename()):
            pass  # Config is already present
        elif self.env == ApiEnvironmentType.SANDBOX:
            sandbox_user = self.generate_new_sandbox_user()
            ApiContext.create(ApiEnvironmentType.SANDBOX,
                              sandbox_user.api_key,
                              socket.gethostname()
                              ).save(self.determine_bunq_conf_filename())
        else:
            raise BunqException(self._ERROR_COULD_NOT_DETERMINE_CONF)

        try:
            api_context = ApiContext.restore(self.determine_bunq_conf_filename())
            api_context.ensure_session_active()
            api_context.save(self.determine_bunq_conf_filename())

            BunqContext.load_api_context(api_context)
        except ForbiddenException as forbidden_exception:
            if reset_config_if_needed:
                self.__handle_forbidden_exception(forbidden_exception)
            else:
                raise forbidden_exception

    def determine_bunq_conf_filename(self):
        if self.env == ApiEnvironmentType.PRODUCTION:
            return self._BUNQ_CONF_PRODUCTION
        else:
            return self._BUNQ_CONF_SANDBOX

    def __handle_forbidden_exception(self, forbidden_exception):
        if self.env == ApiEnvironmentType.SANDBOX:
            remove(self.determine_bunq_conf_filename())
            self.setup_context(False)
        else:
            raise forbidden_exception

    def setup_current_user(self):
        user = User.get().value.get_referenced_object()
        if (
                isinstance(user, UserPerson) or
                isinstance(user, UserCompany) or
                isinstance(user, UserLight)
        ):
            self.user = user

    def update_context(self):
        BunqContext.api_context().save(self.determine_bunq_conf_filename())

    def get_current_user(self) -> Union[UserCompany, UserPerson]:
        return self.user

    def get_all_monetary_account_active(self, count: int = _DEFAULT_COUNT) -> List[MonetaryAccountBank]:
        pagination = Pagination()
        pagination.count = count

        all_monetary_account_bank = MonetaryAccountBank.list(
            pagination.url_params_count_only).value
        all_monetary_account_bank_active = []

        for monetary_account_bank in all_monetary_account_bank:
            if monetary_account_bank.status == \
                    self._MONETARY_ACCOUNT_STATUS_ACTIVE:
                all_monetary_account_bank_active.append(monetary_account_bank)

        return all_monetary_account_bank_active

    def get_all_payment(self, count: int = _DEFAULT_COUNT) -> List[Payment]:
        pagination = Pagination()
        pagination.count = count

        return Payment.list(params=pagination.url_params_count_only).value

    def get_all_request(self, count: int = _DEFAULT_COUNT) -> List[RequestInquiry]:
        pagination = Pagination()
        pagination.count = count

        return RequestInquiry.list(params=pagination.url_params_count_only).value

    def get_all_card(self, count: int = _DEFAULT_COUNT) -> List[Card]:
        pagination = Pagination()
        pagination.count = count

        return Card.list(pagination.url_params_count_only).value

    def make_payment(self, amount_string: str, description: str, recipient: str):
        Payment.create(
            amount=Amount(amount_string, self._CURRENCY_EUR),
            counterparty_alias=Pointer(self._POINTER_TYPE_EMAIL, recipient),
            description=description
        )

    def make_request(self, amount_string: str, description: str, recipient: str):
        RequestInquiry.create(
            amount_inquired=Amount(amount_string, self._CURRENCY_EUR),
            counterparty_alias=Pointer(self._POINTER_TYPE_EMAIL, recipient),
            description=description,
            allow_bunqme=True
        )

    def link_card(self, card_id: int, account_id: int):
        Card.update(
            card_id=card_id,
            pin_code_assignment=[
                CardPinAssignment(
                    type_=self._CARD_PIN_ASSIGNMENT_TYPE,
                    monetary_account_id=account_id
                )
            ]
        )

    def add_callback_url(self, callback_url: str):
        all_notification_filter_current = NotificationFilterUrlUser.list().value
        all_notification_filter_updated = []

        for notification_filter_url_user in all_notification_filter_current:
            for notification_filter_url in notification_filter_url_user.notification_filters:
                if callback_url == notification_filter_url.notification_target:
                    all_notification_filter_updated.append(notification_filter_url)

        all_notification_filter_updated.append(
            NotificationFilterUrl(NOTIFICATION_CATEGORY_MUTATION, callback_url)
        )

        NotificationFilterUrlUserInternal.create_with_list_response(all_notification_filter_updated)

    def update_account(self, name: str, account_id: int):
        MonetaryAccountBank.update(monetary_account_bank_id=account_id, description=name)

    def get_all_user_alias(self) -> List[Pointer]:
        return self.get_current_user().alias

    def generate_new_sandbox_user(self) -> SandboxUserPerson:
        url = ApiEnvironmentType.SANDBOX.uri_base + "sandbox-user-person"

        headers = {
            'x-bunq-client-request-id': "uniqueness-is-required",
            'cache-control': "no-cache",
            'x-bunq-geolocation': "0 0 0 0 NL",
            'x-bunq-language': "en_US",
            'x-bunq-region': "en_US",
        }

        response = requests.request("POST", url, headers=headers)

        if response.status_code is 200:
            response_json = json.loads(response.text)
            return SandboxUserPerson.from_json(json.dumps(response_json["Response"][0]["ApiKey"]))

        raise BunqException(self._ERROR_COULD_NOT_CREATE_NEW_SANDBOX_USER)

    def __request_spending_money_if_needed(self):
        if self.__should_request_spending_money():
            RequestInquiry.create(
                amount_inquired=Amount(self._REQUEST_SPENDING_MONEY_AMOUNT, self._CURRENCY_EUR),
                counterparty_alias=Pointer(self._POINTER_TYPE_EMAIL, self._REQUEST_SPENDING_MONEY_RECIPIENT),
                description=self._REQUEST_SPENDING_MONEY_DESCRIPTION,
                allow_bunqme=False
            )
            sleep(self._REQUEST_SPENDING_MONEY_WAIT_TIME_SECONDS)

    def __should_request_spending_money(self):
        return self.env == ApiEnvironmentType.SANDBOX \
               and float(BunqContext.user_context().primary_monetary_account.balance.value) <= self._ZERO_BALANCE
