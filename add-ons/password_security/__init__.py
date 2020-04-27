# Copyright 2015 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from . import controllers
from . import models


def install_dependecies(cr):
    import os
    os.system("pip3 install wheel")
    os.system("pip3 install zxcvbn-python")


