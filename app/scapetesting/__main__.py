foo = "scapetesting"

import sys
mod = __import__(foo)
sys.modules[foo]=mod

__package__=foo

from .bar import hello

