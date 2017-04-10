import os,sys

# Get File  name without path
print(os.path.basename(__file__))
print(__file__)
print(os.path.basename(__file__).split('.')[0] + '.log')

import TisLib
import TisLib.Routes_Cap
import TisLib.Points_Cap

import Trg_Test.Constants as trg

print(trg.a)