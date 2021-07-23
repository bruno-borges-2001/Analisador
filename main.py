from Operations import *
from Grammar import *
from AF import *
from ER import *

er = ER("(((33|2)(13)*(12|3)|32|1)((23|1)(13)*(12|3)|22)*((23|1)(13)*(11|2)|21|3)|(33|2)(13)*(11|2)|31)*")

er.get_tree()
