import re

sh_ver = '''
pynetauto-rtr011#show version
Cisco IOS XE Software, Version 17.03.01prd8
Cisco IOS Software [Amsterdam], c8000be Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.1prd8, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2020 by Cisco Systems, Inc.
Compiled Tue 19-May-20 12:00 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2020 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: (c)


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.


Technology Package License Information:


Technology Package License Information:

-----------------------------------------------------------------
Technology     Type         Technology-package Technology-package
                            Current            Next Reboot
-----------------------------------------------------------------
Smart License  Perpetual    network-essentials network-essentials
Smart License  Subscription None               None

The current crypto throughput level is 1000000 kbps


cisco C8300-1N1S-6T (1RU) processor with 3763048K/6148K bytes of memory.
Processor board ID FDO1353B0CF
Router operating mode: Autonomous
6 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
7090175K bytes of flash memory at bootflash:.
28884992K bytes of M.2 USB at harddisk:.

Configuration register is 0x2102
'''

# Only match Cisco model number from 'show version' output.
# Adding the 'r' prefix to treat the backslashes as literal characters and not as escape sequences
rtr_model = re.findall(r'C\d{4}[^\s]+', sh_ver) 
router_model = rtr_model[0]
print(router_model)