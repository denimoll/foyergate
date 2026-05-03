"""FoyerGate — an OSS supply chain gateway.

Vet open-source packages before they enter your local repository.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

try:
    __version__ = _pkg_version("foyergate")
except PackageNotFoundError:  # not installed (e.g. running from source tree)
    __version__ = "0.0.0+local"
