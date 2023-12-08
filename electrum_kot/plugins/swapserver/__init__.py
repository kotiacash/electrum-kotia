from electrum_kot.i18n import _

fullname = _('SwapServer')
description = """
Submarine swap server for an Electrum daemon.

Example setup:

  electrum-kot -o setconfig use_swapserver True
  electrum-kot -o setconfig swapserver_address localhost:5455
  electrum-kot daemon -v

"""

available_for = ['cmdline']
