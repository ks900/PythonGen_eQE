#!/usr/bin/env python

import sys
import shutil
import fileinput
import os
from os import walk
import string
import subprocess
import time
import errno
import imp
from itertools import chain
import argparse
#from argsparse import ArugmentParser, REMAINDER 
from os.path import expanduser



####
### Tell us here what type of files u would like created.
##  Below are listed options for which frag charge files to create.
#
# zero- 0.0 / 1.0
# one - 1.0 / 0.0
# five- 0.5 / 0.5
# zo - zero and one
# zf - zero and five
# of - one and five
# zfo - zero one and five
#
## Input one of these values as a part of the arguments. 
###
####



os.system("python updated_ks_autogen.py -d a1 -p /home/khurshid/QE/QE_Submission_Script -f zfo")
