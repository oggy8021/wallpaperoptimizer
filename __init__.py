"""harite.WallpaperOptimizer package

This __init__ flattens the nested `WallpaperOptimizer/WallpaperOptimizer` layout
by prepending the inner directory to the package search path. Consumers can
import `harite.WallpaperOptimizer.Core` etc. without the extra nested name.
"""

import os
__all__ = []

# Prepend inner package folder to this package's __path__ so that modules
# under WallpaperOptimizer/WallpaperOptimizer/ become available directly as
# harite.WallpaperOptimizer.<module>
inner_dir = os.path.join(os.path.dirname(__file__), 'WallpaperOptimizer')
if os.path.isdir(inner_dir):
    __path__.insert(0, inner_dir)

# Optionally import common names to make IDEs/repl happier (best-effort)
try:
    from . import Core as Core  # noqa: F401
    from . import Config as Config  # noqa: F401
    from . import WorkSpace as WorkSpace  # noqa: F401
except Exception:
    # ignore import errors at package import time
    pass

# Re-export some top-level metadata/constants from the inner package if present
try:
    import importlib
    _inner = importlib.import_module(__name__ + '.WallpaperOptimizer')
    for _attr in ('USERENVDIR', 'WINDOWMANAGER', 'VERSION', 'AUTHOR', 'ICONDIR', 'LIBRARYDIR'):
        if hasattr(_inner, _attr):
            globals()[_attr] = getattr(_inner, _attr)
except Exception:
    pass
