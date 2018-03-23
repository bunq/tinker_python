#!.venv/bin/python -W ignore
from libs.bunq_lib import BunqLib
from libs.share_lib import ShareLib
from bunq.sdk.context import ApiEnvironmentType


def main():
    all_option = ShareLib.parse_all_option()
    environment_type = ShareLib.determine_environment_type_from_all_option(all_option)

    ShareLib.print_header()

    bunq = BunqLib(environment_type)

    user = bunq.get_current_user()
    ShareLib.print_user(user)

    all_monetary_account_bank_active = bunq.get_all_monetary_account_active(1)
    ShareLib.print_all_monetary_account_bank(all_monetary_account_bank_active)

    all_payment = bunq.get_all_payment(1)
    ShareLib.print_all_payment(all_payment)

    all_request = bunq.get_all_request(1)
    ShareLib.print_all_request(all_request)

    all_card = bunq.get_all_card(1)
    ShareLib.print_all_card(all_card, all_monetary_account_bank_active)

    if environment_type is ApiEnvironmentType.SANDBOX:
        all_alias = bunq.get_all_user_alias()
        ShareLib.print_all_user_alias(all_alias)

    bunq.update_context()

    print("""


   Want to see more monetary accounts, payments, requests or even cards?
   Adjust this file.


""")

if __name__ == '__main__':
    main()
