from pas.plugins.passwordstrength import PLUGIN_ID
from plone import api

import pytest


class TestPlugin:
    @pytest.fixture(autouse=True)
    def _initialize(self, portal, http_request):
        self.pas = api.portal.get_tool("acl_users")
        self.plugin = getattr(self.pas, PLUGIN_ID)
        self.http_request = http_request
        self.http_response = http_request.response

    @pytest.mark.parametrize(
        "property,expected",
        [
            # ("p1_re", True),
            ("p1_err", "Minimum 8 characters"),
        ],
    )
    def test_plugin_setup(self, property, expected):
        plugin = self.plugin
        assert plugin.getProperty(property) == expected
