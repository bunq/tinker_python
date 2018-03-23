#!.venv/bin/python -W ignore
from libs.bunq_lib import BunqLib
from libs.share_lib import ShareLib

def main():
    all_option = ShareLib.parse_all_option()
    environment_type = ShareLib.determine_environment_type_from_all_option(all_option)

    ShareLib.print_header()

    bunq = BunqLib(environment_type)

    card_id = ShareLib.determine_card_id_from_all_option_or_std_in(all_option)
    account_id = ShareLib.determine_account_id_from_all_option_or_std_in(all_option)

    print(f'''
  | Link Card:    {card_id}
  | To Account:   {account_id}
   
    ...
''')

    bunq.link_card(card_id, account_id)

    print('''
  | ✅  Account switched

  | ▶  Check your changed overview

''')

    bunq.update_context()

if __name__ == '__main__':
    main()
