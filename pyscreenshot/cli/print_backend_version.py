import logging
from pyscreenshot.loader import backend_version2

log = logging.getLogger(__name__)


def main(backend):
    """Print pyscreenshot back-end version.
    :param backend: back-end (example:scrot, wx,..)
    """
    backend = backend if backend else None

    try:
        v = backend_version2(backend)
    except Exception as e:
        log.warning(e)
        v = ""
    print(v)
