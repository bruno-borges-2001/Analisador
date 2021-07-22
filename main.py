from Operations import *
from Grammar import *
from AF import *
from ER import *

er = ER("ab(ca)*|c(a|b)*|a*b")

er.get_tree()
