from Operations import *
from Grammar import *
from AF import *
from ER import *

er = ER("(0-3|6-7)*|a(4-5)b*")

afd = er.get_afd(True)
