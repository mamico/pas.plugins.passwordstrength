from pas.plugins.passwordstrength import PLUGIN_ID
from plone import api

import pytest


class TestFunctionalPlugin:
    @pytest.fixture(autouse=True)
    def _initialize(self, portal):
        pas = api.portal.get_tool("acl_users")
        plugin = getattr(pas, PLUGIN_ID)
        self.portal_url = api.portal.get().absolute_url()
        self.plugin_url = plugin.absolute_url()

    # must_change_password
    # login
    #  ...