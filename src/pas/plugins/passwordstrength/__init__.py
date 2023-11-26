# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


_ = MessageFactory("pas.plugins.passwordstrength")
logger = logging.getLogger("pas.plugins.passwordstrength")
PLUGIN_ID = "passwordstrength_policy"
