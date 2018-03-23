#!.venv/bin/python -W ignore
from libs.bunq_lib import BunqLib
from libs.share_lib import ShareLib

def main():
    all_option = ShareLib.parse_all_option()
    environment_type = ShareLib.determine_environment_type_from_all_option(all_option)

    ShareLib.print_header()

    bunq = BunqLib(environment_type)

    amount = ShareLib.determine_amount_from_all_option_or_std_in(all_option)
    description = ShareLib.determine_description_from_all_option_or_std_in(all_option)
    recipient = ShareLib.determine_recipient_from_all_option_or_std_in(all_option)

    print(f'''
  | Requesting:   € {amount}
  | From:         {recipient}
  | Description:  {description}
   
    ...
''')

    bunq.make_request(amount, description, recipient)

    print('''
  | ✅  Request sent

  | ▶  Check your changed overview

''')

    bunq.update_context()

if __name__ == '__main__':
    main()
