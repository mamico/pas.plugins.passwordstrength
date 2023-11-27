from pas.plugins.passwordstrength import PACKAGE_NAME
from plone import api

import pytest


class TestSetupInstall:
    @pytest.fixture(autouse=True)
    def _initialize(self, portal):
        self.portal = portal

    def test_addon_installed(self, installer):
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1000"

    def test_browserlayer(self, browser_layers):
        """Test that IPasPluginsPasswordstrengthLayer is registered."""
        from pas.plugins.passwordstrength.interfaces import (
            IPasPluginsPasswordstrengthLayer,
        )

        assert IPasPluginsPasswordstrengthLayer in browser_layers

    def test_plugin_added(self):
        """Test if plugin is added to acl_users."""
        from pas.plugins.passwordstrength import PLUGIN_ID

        pas = api.portal.get_tool("acl_users")
        assert PLUGIN_ID in pas.objectIds()

    def test_plugin_is_passwordstrength(self):
        """Test if we have the correct plugin."""
        from pas.plugins.passwordstrength import PLUGIN_ID
        from pas.plugins.passwordstrength.plugins import PasswordStrength

        pas = api.portal.get_tool("acl_users")
        plugin = getattr(pas, PLUGIN_ID)
        assert isinstance(plugin, PasswordStrength)
