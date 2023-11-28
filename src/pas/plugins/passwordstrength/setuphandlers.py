from pas.plugins.passwordstrength import logger
from pas.plugins.passwordstrength import PLUGIN_ID
from pas.plugins.passwordstrength.plugins import PasswordStrength
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "pas.plugins.passwordstrength:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["pas.plugins.passwordstrength.upgrades"]


def post_install(context):
    """Post install script"""
    pas = api.portal.get_tool("acl_users")

    # Create plugin if it does not exist.
    if PLUGIN_ID not in pas.objectIds():
        plugin = PasswordStrength(
            id=PLUGIN_ID,
            title="Create your own rules for enforcing password strength",
        )
        pas._setObject(PLUGIN_ID, plugin)
        logger.info("Created %s in acl_users.", PLUGIN_ID)
    plugin = getattr(pas, PLUGIN_ID)
    if not isinstance(plugin, PasswordStrength):
        raise ValueError(f"Existing PAS plugin {PLUGIN_ID} is not a PasswordStrength.")

    activate_challenge_plugin(context)
    activate_validation_plugin(context)
    
    return plugin


def activate_plugin(context, interface_name, move_to_top=False):
    pas = api.portal.get_tool("acl_users")
    if PLUGIN_ID not in pas.objectIds():
        raise ValueError(f"acl_users has no plugin {PLUGIN_ID}.")

    plugin = getattr(pas, PLUGIN_ID)
    if not isinstance(plugin, PasswordStrength):
        raise ValueError(f"Existing PAS plugin {PLUGIN_ID} is not a PasswordStrength.")

    # This would activate one interface and deactivate all others:
    # plugin.manage_activateInterfaces([interface_name])
    # So only take over the necessary code from manage_activateInterfaces.
    plugins = pas.plugins
    iface = plugins._getInterfaceFromName(interface_name)
    if PLUGIN_ID not in plugins.listPluginIds(iface):
        plugins.activatePlugin(iface, PLUGIN_ID)
        logger.info(f"Activated interface {interface_name} for plugin {PLUGIN_ID}")

    if move_to_top:
        # Order some plugins to make sure our plugin is at the top.
        # This is not needed for all plugin interfaces.
        plugins.movePluginsTop(iface, [PLUGIN_ID])
        logger.info(f"Moved {PLUGIN_ID} to top of {interface_name}.")


def activate_challenge_plugin(context):
    activate_plugin(context, "IChallengePlugin", move_to_top=True)


def activate_validation_plugin(context):
    activate_plugin(context, "IValidationPlugin", move_to_top=True)


def uninstall(context):
    """Uninstall script"""
    pas = api.portal.get_tool("acl_users")

    # Remove plugin if it exists.
    if PLUGIN_ID not in pas.objectIds():
        return

    plugin = getattr(pas, PLUGIN_ID)
    if not isinstance(plugin, PasswordStrength):
        logger.warning(
            f"PAS plugin {PLUGIN_ID} not removed: it is not a PasswordStrength."
        )
        return
    pas._delObject(PLUGIN_ID)
    logger.info(f"Removed PasswordStrength {PLUGIN_ID} from acl_users.")
