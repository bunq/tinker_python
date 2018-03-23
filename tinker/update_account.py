#!.venv/bin/python -W ignore
from libs.bunq_lib import BunqLib
from libs.share_lib import ShareLib

def main():
    all_option = ShareLib.parse_all_option()
    environment_type = ShareLib.determine_environment_type_from_all_option(all_option)

    ShareLib.print_header()

    bunq = BunqLib(environment_type)

    account_id = ShareLib.determine_account_id_from_all_option_or_std_in(all_option)
    name = ShareLib.determine_name_from_all_option_or_std_in(all_option)

    print(f'''
  | Updating Name:      {name}
  | of Account:         {account_id}
   
    ...
''')

    bunq.update_account(name, account_id)

    print('''
  | ✅  Account updated

  | ▶  Check your changed overview

''')

    bunq.update_context()

if __name__ == '__main__':
    main()
