from .base import *

# live = False

try:
    from .local import *
    live = False
except:
    from .production import *
    live = True

# if live:
#     from .production import *
# else:
#     from .local import *