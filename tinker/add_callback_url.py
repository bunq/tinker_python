#!.venv/bin/python -W ignore
from libs.bunq_lib import BunqLib
from libs.share_lib import ShareLib

def main():
    all_option = ShareLib.parse_all_option()
    environment_type = ShareLib.determine_environment_type_from_all_option(all_option)

    ShareLib.print_header()

    bunq = BunqLib(environment_type)

    callback_url = ShareLib.determine_callback_url_from_all_option_or_std_in(all_option)

    print(f'''
  | Adding Callback URL:    {callback_url}
   
    ...
''')

    bunq.add_callback_url(callback_url)

    print('''
  | ✅  Callback URL added

  | ▶  Check your changed overview

''')

    bunq.update_context()

if __name__ == '__main__':
    main()
