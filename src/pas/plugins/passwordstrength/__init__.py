"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


PLUGIN_ID = "passwordstrength_policy"
PACKAGE_NAME = "pas.plugins.passwordstrength"

_ = MessageFactory(PACKAGE_NAME)
logger = logging.getLogger(PACKAGE_NAME)
