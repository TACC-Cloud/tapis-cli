import os
from tapis_cli import settings
from tapis_cli.utils import prompt_accept
from tapis_cli.commands.local.settings.set import settings_set

__all__ = ['firstrun']


def display_aup():
    print('''
Use of Tapis requires acceptance of the TACC Acceptable Use Policy,
which can be found at https://portal.tacc.utexas.edu/tacc-usage-policy
''')
    return prompt_accept('Do you agree to abide by the AUP?',
                         None,
                         exit_reject=True)


def opt_in_reporting():
    print('''
To improve our ability to support Tapis and the Tapis CLI, we would like to
collect your IP addrress, operating system and Python version. No personally-
identifiable information will be collected. This data will only be shared in
aggregate form with funders and Tapis platform stakeholders.
''')
    return prompt_accept('Do you consent to this reporting?',
                         'y',
                         exit_reject=False)


def firstrun_file():
    return os.path.expanduser('~/.tapis_firstrun')


def touch_firstrun():
    with open(firstrun_file(), 'w') as f:
        f.write('')
        f.close()


def exist_firstrun():
    return os.path.exists(firstrun_file())


def firstrun():
    """First-run workflow
    """
    if not exist_firstrun():
        if settings.TAPIS_CLI_DISPLAY_AUP:
            display_aup()
        if settings.TAPIS_CLI_GA_DISABLE is False:
            if not opt_in_reporting():
                settings_set('TAPIS_CLI_GA_DISABLE', 'true')
        touch_firstrun()
