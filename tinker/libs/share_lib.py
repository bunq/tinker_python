import argparse
import os
import sys

from bunq.sdk.context import ApiEnvironmentType
from bunq.sdk.exception import BunqException
from bunq.sdk.model.generated import endpoint
from bunq.sdk.model.generated import object_


class ShareLib(object):
    _ERROR_COULD_NOT_FIND_IBAN_POINTER = 'Could not determine IBAN for Monetary Account.'

    _OPTION_PRODUCTION = '--production'
    _OPTION_AMOUNT = '--amount'
    _OPTION_DESCRIPTION = '--description'
    _OPTION_RECIPIENT = '--recipient'
    _OPTION_CARD_ID = '--card-id'
    _OPTION_ACCOUNT_ID = '--account-id'
    _OPTION_CALLBACK_URL = '--callback-url'
    _OPTION_NAME = '--name'

    _ECHO_USER = os.linesep + '   User'
    _ECHO_MONETARY_ACCOUNT = os.linesep + '   Monetary Accounts'
    _ECHO_PAYMENT = os.linesep + '   Payments'
    _ECHO_REQUEST = os.linesep + '   Request'
    _ECHO_CARD = os.linesep + '   Card'
    _ECHO_AMOUNT_IN_EUR = os.linesep + '    Amount (EUR): '
    _ECHO_DESCRIPTION = os.linesep + '    Description: '
    _ECHO_RECIPIENT = os.linesep + '    Recipient (%s): '
    _ECHO_CARD_ID = os.linesep + '    Card (ID): '
    _ECHO_ACCOUNT_ID = os.linesep + '    Account (ID): '
    _ECHO_CALLBACK_URL = os.linesep + '    Callback URL: '
    _ECHO_NEW_NAME = os.linesep + '    New Name: '

    _DEFAULT_CARD_SECOND_LINE = 'bunq card'
    _DEFAULT_RECIPIENT_EMAIL = 'e.g. bravo@bunq.com'

    _POINTER_TYPE_EMAIL = 'EMAIL'
    _POINTER_TYPE_IBAN = 'IBAN'

    environment_type = None

    @classmethod
    def parse_all_option(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument(cls._OPTION_PRODUCTION, action='store_true')
        parser.add_argument(cls._OPTION_AMOUNT)
        parser.add_argument(cls._OPTION_DESCRIPTION)
        parser.add_argument(cls._OPTION_RECIPIENT)
        parser.add_argument(cls._OPTION_CARD_ID)
        parser.add_argument(cls._OPTION_ACCOUNT_ID)
        parser.add_argument(cls._OPTION_CALLBACK_URL)
        parser.add_argument(cls._OPTION_NAME)
        return parser.parse_args()

    @classmethod
    def determine_environment_type_from_all_option(cls, all_option):
        """
        :rtype: ApiEnvironmentType
        """

        if all_option.production:
            cls.environment_type = ApiEnvironmentType.PRODUCTION
        else:
            cls.environment_type = ApiEnvironmentType.SANDBOX

        return cls.environment_type

    @classmethod
    def determine_amount_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str
        """

        if all_option.amount:
            return all_option.amount
        else:
            print(cls._ECHO_AMOUNT_IN_EUR, end='')

            return sys.stdin.readline().strip()

    @classmethod
    def determine_description_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str
        """

        if all_option.description:
            return all_option.description
        else:
            print(cls._ECHO_DESCRIPTION, end='')

            return sys.stdin.readline().strip()

    @classmethod
    def determine_recipient_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str

        """
        if all_option.recipient:
            return all_option.recipient
        else:
            if ApiEnvironmentType.SANDBOX == cls.environment_type:
                input_hint = cls._DEFAULT_RECIPIENT_EMAIL
            else:
                input_hint = cls._POINTER_TYPE_EMAIL

            print(cls._ECHO_RECIPIENT % input_hint, end='')
            return sys.stdin.readline().strip()

    @classmethod
    def determine_card_id_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str
        """

        if all_option.card_id:
            return all_option.card_id
        else:
            print(cls._ECHO_CARD_ID, end='')

            return sys.stdin.readline().strip()

    @classmethod
    def determine_account_id_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str
        """

        if all_option.account_id:
            return all_option.account_id
        else:
            print(cls._ECHO_ACCOUNT_ID, end='')

            return sys.stdin.readline().strip()

    @classmethod
    def determine_callback_url_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str
        """

        if all_option.callback_url:
            return all_option.callback_url
        else:
            print(cls._ECHO_CALLBACK_URL, end='')
            return sys.stdin.readline().strip()
        pass

    @classmethod
    def determine_name_from_all_option_or_std_in(cls, all_option):
        """
        :rtype: str
        """

        if all_option.name:
            return all_option.name
        else:
            print(cls._ECHO_NEW_NAME, end='')

            return sys.stdin.readline().strip()
        pass

    @classmethod
    def print_header(cls):
        if ApiEnvironmentType.SANDBOX == cls.environment_type:
            print("""
\033[94m
  ████████╗██╗███╗   ██╗██╗  ██╗███████╗██████╗ ██╗███╗   ██╗ ██████╗ 
  ╚══██╔══╝██║████╗  ██║██║ ██╔╝██╔════╝██╔══██╗██║████╗  ██║██╔════╝ 
     ██║   ██║██╔██╗ ██║█████╔╝ █████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗
     ██║   ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║
     ██║   ██║██║ ╚████║██║  ██╗███████╗██║  ██║██║██║ ╚████║╚██████╔╝
     ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
\033[0m
            """)
        else:
            print("""
\033[93m
  ██████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
  ██████╔╝██████╔╝██║   ██║██║  ██║██║   ██║██║        ██║   ██║██║   ██║██╔██╗ ██║
  ██╔═══╝ ██╔══██╗██║   ██║██║  ██║██║   ██║██║        ██║   ██║██║   ██║██║╚██╗██║
  ██║     ██║  ██║╚██████╔╝██████╔╝╚██████╔╝╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
\033[0m
            """)

    @classmethod
    def print_user(cls, user):
        """

        :param user: UserPerson|UserCompany|UserLight
        """

        print(cls._ECHO_USER)
        print(f'''
  ┌────────────────┬───────────────────────────────────────────────────────
  │ ID             │ {user.id_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Username       │ {user.display_name}
  └────────────────┴───────────────────────────────────────────────────────''')

    @classmethod
    def print_all_monetary_account_bank(cls, all_monetary_account_bank):
        """
        :type all_monetary_account_bank: list[endpoint.MonetaryAccountBank]
        """

        print(cls._ECHO_MONETARY_ACCOUNT)

        for monetary_account_bank in all_monetary_account_bank:
            cls.print_monetary_account_bank(monetary_account_bank)

    @classmethod
    def print_monetary_account_bank(cls, monetary_account_bank):
        """
        :param monetary_account_bank: MonetaryAccountBank
        """

        pointer_iban = cls.get_first_pointer_iban(monetary_account_bank)

        print(f'''
  ┌────────────────┬───────────────────────────────────────────────────────
  │ ID             │ {monetary_account_bank.id_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Description    │ {monetary_account_bank.description}
  ├────────────────┼───────────────────────────────────────────────────────
  │ IBAN           │ {pointer_iban.value}''')

        if monetary_account_bank.balance is not None:
            print(f'''  ├────────────────┼───────────────────────────────────────────────────────
  │ Balance        │ {monetary_account_bank.balance.currency} {monetary_account_bank.balance.value}''')

        print(
            f'  └────────────────┴───────────────────────────────────────────────────────')

    @classmethod
    def get_first_pointer_iban(cls, monetary_account_bank):
        """
        :rtype: object_.Pointer
        """

        for alias in monetary_account_bank.alias:
            if alias.type_ == cls._POINTER_TYPE_IBAN:
                return alias

        raise BunqException(cls._ERROR_COULD_NOT_FIND_IBAN_POINTER)

    @classmethod
    def print_all_payment(cls, all_payment):
        """
        :type all_payment: list[endpoint.Payment]
        """

        print(cls._ECHO_PAYMENT)

        for payment in all_payment:
            cls.print_payment(payment)

    @classmethod
    def print_payment(cls, payment):
        """
        :type payment: endpoint.Payment
        """

        print(f'''
  ┌────────────────┬───────────────────────────────────────────────────────
  │ ID             │ {payment.id_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Description    │ {payment.description}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Amount         │ {payment.amount.currency} {payment.amount.value}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Recipient      │ {payment.counterparty_alias.label_monetary_account.display_name}
  └────────────────┴───────────────────────────────────────────────────────''')

    @classmethod
    def print_all_request(cls, all_request):
        """
        :type all_request: list[endpoint.RequestInquiry]
        """

        print(cls._ECHO_REQUEST)

        for request in all_request:
            cls.print_request(request)

    @classmethod
    def print_request(cls, request):
        """
        :type request: endpoint.RequestInquiry
        """

        print(f'''
  ┌────────────────┬───────────────────────────────────────────────────────
  │ ID             │ {request.id_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Description    │ {request.description}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Status         │ {request.status}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Amount         │ {request.amount_inquired.currency} {request.amount_inquired.value}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Recipient      │ {request.counterparty_alias.label_monetary_account.display_name}
  └────────────────┴───────────────────────────────────────────────────────''')

    @classmethod
    def print_all_card(cls, all_card, all_monetary_account):
        """
        :param all_card: list(endpoint.Card)
        :param all_monetary_account: list[endpoint.MonetaryAccountBank]
        """

        print(cls._ECHO_CARD)

        for card in all_card:
            cls.print_card(card, all_monetary_account)

    @classmethod
    def print_card(cls, card, all_monetary_account):
        """
        :type card: endpoint.Card
        :type all_monetary_account: list[endpoint.MonetaryAccountBank]
        """

        if card.label_monetary_account_current is None:
            linked_account = 'No account linked yet.'
        else:
            monetary_account = cls.get_monetary_account_from_label(
                card.label_monetary_account_current.label_monetary_account,
                all_monetary_account
            )
            linked_account = f'{monetary_account.description} ' \
                f'({card.label_monetary_account_current.label_monetary_account.iban})'

        print(f'''
  ┌────────────────┬───────────────────────────────────────────────────────
  │ ID             │ {card.id_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Type           │ {card.type_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Name on Card   │ {card.name_on_card}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Description    │ {card.second_line or cls._DEFAULT_CARD_SECOND_LINE}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Linked Account │ {linked_account}
  └────────────────┴───────────────────────────────────────────────────────''')

    @classmethod
    def get_monetary_account_from_label(cls, label_monetary_account_current,
                                        all_monetary_account):
        """
        :type label_monetary_account_current: object_.LabelMonetaryAccount
        :type all_monetary_account: list[endpoint.MonetaryAccountBank]
        """

        iban_label = label_monetary_account_current.iban

        for monetary_account in all_monetary_account:
            iban_monetary_account = cls.get_first_pointer_iban(
                monetary_account).value

            if iban_label == iban_monetary_account:
                return monetary_account

        return None

    @staticmethod
    def print_all_user_alias(all_user_alias):
        """
        :type all_user_alias: list[object_.Pointer]
        """

        print("\n" + "   You can use these login credentials to login in to "
                     "the bunq sandbox app.")

        for alias in all_user_alias:
            print(f'''
  ┌────────────────┬───────────────────────────────────────────────────────
  │ Value          │ {alias.value}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Type           │ {alias.type_}
  ├────────────────┼───────────────────────────────────────────────────────
  │ Login Code     │ 000000
  └────────────────┴───────────────────────────────────────────────────────''')
