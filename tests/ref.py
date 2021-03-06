import logging
import sys
import os

import pyscreenshot
import six
from easyprocess import EasyProcess
from nose.tools import eq_, ok_
from path import TempDir
from PIL import Image, ImageChops
from pyscreenshot.util import platform_is_osx

import fillscreen
from config import bbox_ls
from image_debug import img_debug
from size import backend_size


def check_ref(backend, bbox, childprocess, refimgpath):
    img_ref = Image.open(refimgpath)
    logging.debug("ref full getextrema: %s", img_ref.getextrema())
    if bbox:
        img_ref = img_ref.crop(bbox)

    im = pyscreenshot.grab(bbox=bbox, backend=backend, childprocess=childprocess)

    img_ref = img_ref.convert("RGB")
    logging.debug("ref  getextrema: %s", img_ref.getextrema())
    im = im.convert("RGB")
    logging.debug("shot getextrema: %s", im.getextrema())

    eq_("RGB", img_ref.mode)
    eq_("RGB", im.mode)

    img_debug(img_ref, "ref" + str(bbox))
    img_debug(im, str(backend) + str(bbox))

    img_diff = ImageChops.difference(img_ref, im)
    ex = img_diff.getextrema()
    logging.debug("diff getextrema: %s", ex)
    diff_bbox = img_diff.getbbox()
    if diff_bbox:
        img_debug(img_diff, "img_diff" + str(diff_bbox))
    if (
        platform_is_osx()
        and backend
        and backend in ["qtpy", "pyqt", "pyqt5", "pyside", "pyside2"]
    ):
        # TODO: qt color problem on osx
        color_diff_max = max([b for (_, b) in ex])
        ok_(color_diff_max < 70)
    else:
        eq_(
            diff_bbox,
            None,
            "different image data %s bbox=%s extrema:%s diff_bbox=%s"
            % (backend, bbox, ex, diff_bbox),
        )


def backend_ref(backend, childprocess=True, refimgpath=""):
    for bbox in bbox_ls:
        print("bbox: {}".format(bbox))
        print("backend: %s" % backend)
        check_ref(backend, bbox, childprocess, refimgpath)


def _backend_check(backend, childprocess, refimgpath):
    enable_ref = bool(refimgpath)
    if enable_ref:
        backend_ref(
            backend, childprocess=childprocess, refimgpath=refimgpath,
        )
    else:
        backend_size(
            backend, childprocess=childprocess,
        )


def backend_to_check(backend):
    refimgpath = fillscreen.init()
    _backend_check(backend, childprocess=None, refimgpath=refimgpath)
    # _backend_check(backend, childprocess=False) # TODO: test childprocess=True/False/auto


def check_import(module):
    # TODO: check without importing, use in plugins also
    found = False
    # try:
    #     __import__(module)

    #     ok = True
    # except ImportError:
    #     pass
    if six.PY2:
        import imp

        try:
            imp.find_module(module)
            found = True
        except ImportError:
            found = False
    else:
        import importlib

        spam_spec = importlib.util.find_spec(module)
        found = spam_spec is not None
    return found


def prog_check(cmd):
    try:
        if EasyProcess(cmd).call().return_code == 0:
            return True
    except Exception:
        return False


def kde():
    XDG_CURRENT_DESKTOP = os.environ.get("XDG_CURRENT_DESKTOP")
    if XDG_CURRENT_DESKTOP:
        return "kde" in XDG_CURRENT_DESKTOP.lower()


def gnome():
    XDG_CURRENT_DESKTOP = os.environ.get("XDG_CURRENT_DESKTOP")
    if XDG_CURRENT_DESKTOP:
        return "gnome" in XDG_CURRENT_DESKTOP.lower()
