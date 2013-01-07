'''
@summary: Main module, doesn't hold much logic.
Don't import this, as it relies on sys being already imported in the C code
'''
# pyreshark.py
#
# Pyreshark Plugin for Wireshark. (https://github.com/pyreshark/PyreShark)
#
# Copyright (c) 2013 by Eshed Shaham.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import os.path
from glob import glob

PYRESHARK_DIR = sys.path[-1]
PROTOCOLS_DIR = os.path.join(PYRESHARK_DIR, "protocols")


# The following is to handle the situation where the user doesn't have enough privileges to open the logs.
try:
    sys.stdout = open("%s\\out.log" % sys.path[-1],"wb")
    sys.stderr = open("%s\\err.log" % sys.path[-1],"wb")
except:
    pass

sys.path.append(PROTOCOLS_DIR)
    
import cal

class PyreShark(object):
    '''
    @summary: A class holding the main routines for pyreshark
    '''
    def __init__(self):
        '''
        @summary: Initializes the CAL, instantiates the python plugins and registers them.
        '''
        self._protocols = []
        self._cal = cal.CAL()
        protocol_files = glob("%s\\*.py" % (PROTOCOLS_DIR,))
        
        for p_file in protocol_files:
            proto_module = __import__(p_file.replace("%s\\" % (PROTOCOLS_DIR,), "").replace(".py", ""))
            self._protocols.append(proto_module.Protocol())
        
        self._cal.register_protocols(self._protocols)
        
    def handoff(self):
        '''
        @summary: Calls the handoff function in each one of the protocols.
        '''
        for proto in self._protocols:
            proto.handoff()


if '__main__' == __name__:
    g_pyreshark = PyreShark() #Must be a global so it isn't Auto-Garbage-Collected