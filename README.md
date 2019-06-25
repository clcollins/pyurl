pyurl
=====

Python-based URL shortener

Part of a series of random programs I'm writing in an attempt to learn python. As such,
do not expect any of the code here to be anywhere close to professional standards.

Comments and suggestions welcome. Patches too, but I'll branch them as it would otherwise defeat the purpose.

Files: 
* bin/pyrul.py - the main application, configured for mod_wsgi & Apache
* templates/index.html - the main pyurl template page
* templates/metrics.html - template page for displaying user's Apache log metrics

Requires:
* If you plan to use the rudimentary built in metrics, you'll need to have mod_log_sql installed

Tested with Python 2.6.6 on RHEL 6.

Copyright Information
---------------------
Copyright (C) 2013-2019 Chris Collins

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
