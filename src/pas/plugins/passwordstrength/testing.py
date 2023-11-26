# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pas.plugins.passwordstrength


class PasPluginsPasswordstrengthLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=pas.plugins.passwordstrength)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "pas.plugins.passwordstrength:default")


PAS_PLUGINS_PASSWORDSTRENGTH_FIXTURE = PasPluginsPasswordstrengthLayer()


PAS_PLUGINS_PASSWORDSTRENGTH_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PAS_PLUGINS_PASSWORDSTRENGTH_FIXTURE,),
    name="PasPluginsPasswordstrengthLayer:IntegrationTesting",
)


PAS_PLUGINS_PASSWORDSTRENGTH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PAS_PLUGINS_PASSWORDSTRENGTH_FIXTURE,),
    name="PasPluginsPasswordstrengthLayer:FunctionalTesting",
)


PAS_PLUGINS_PASSWORDSTRENGTH_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PAS_PLUGINS_PASSWORDSTRENGTH_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="PasPluginsPasswordstrengthLayer:AcceptanceTesting",
)
