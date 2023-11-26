# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.Cache import Cacheable
from pas.plugins.passwordstrength import _
from plone import api
from plone.base.utils import safe_text
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin

# from pas.plugins.passwordstrength import logger
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from zope.i18n import translate

import re


PLUGIN_ID = "password_strength_plugin"
PLUGIN_TITLE = _("Create your own rules for enforcing password strength")


def manage_addPasswordStrength(dispatcher, id, title=None, REQUEST=None):
    """Add a PasswordStrength plugin to a Pluggable Auth Service."""

    obj = PasswordStrength(id, title)
    dispatcher._setObject(obj.getId(), obj)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace?manage_tabs_message="
            "PasswordStrength+plugin+added." % dispatcher.absolute_url()
        )


# BBB: i18ndude
_("Minimum 8 characters")
_("Minimum 1 capital letter")
_("Minimum 1 lower case letter")
_("Minimum 1 number")
_("Minimum 1 non-alpha character")

DEFAULT_POLICIES = [
    (r".{8}.*", "Minimum 8 characters"),
    (r".*[A-Z].*", "Minimum 1 capital letter"),
    (r".*[a-z].*", "Minimum 1 lower case letter"),
    (r".*[0-9].*", "Minimum 1 number"),
    (r".*[^0-9a-zA-Z ].*", "Minimum 1 non-alpha character"),
]


class PasswordStrength(BasePlugin, Cacheable):
    """PAS plugin that ensures strong passwords"""

    meta_type = "Password Strength Plugin"
    security = ClassSecurityInfo()

    _properties = (
        {
            "id": "title",
            "label": "Title",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p1_re",
            "label": "Policy 1 Regular Expression",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p1_err",
            "label": "Policy 1 Error Message",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p2_re",
            "label": "Policy 2 Regular Expression",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p2_err",
            "label": "Policy 2 Error Message",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p3_re",
            "label": "Policy 3 Regular Expression",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p3_err",
            "label": "Policy 3 Error Message",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p4_re",
            "label": "Policy 4 Regular Expression",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p4_err",
            "label": "Policy 4 Error Message",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p5_re",
            "label": "Policy 5 Regular Expression",
            "type": "string",
            "mode": "w",
        },
        {
            "id": "p5_err",
            "label": "Policy 5 Error Message",
            "type": "string",
            "mode": "w",
        },
    )

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

        i = 1
        for reg, err in DEFAULT_POLICIES:
            setattr(self, "p%i_re" % i, reg)
            setattr(self, "p%i_err" % i, err)
            i += 1

    security.declarePrivate("validateUserInfo")

    def validateUserInfo(self, user, set_id, set_info):
        """-> ( error_info_1, ... error_info_N )

        o Returned values are dictionaries, containing at least keys:

          'id' -- the ID of the property, or None if the error is not
                  specific to one property.

          'error' -- the message string, suitable for display to the user.
        """

        errors = []
        if set_info and set_info.get("password", None) is not None:
            password = set_info["password"]
            i = 1
            while True:
                reg = self.getProperty(f"p{i}_re", None)
                if not reg:
                    break
                if not re.match(reg, password):
                    err = self.getProperty(f"p{i}_err", None)
                    if err:
                        errors += [
                            translate(
                                safe_text(err),
                                domain="pas.plugins.passwordstrength",
                                context=api.env.getRequest(),
                            )
                        ]
                i += 1

            errors = [{"id": "password", "error": e} for e in errors]
        return errors


classImplements(PasswordStrength, IValidationPlugin)

InitializeClass(PasswordStrength)
