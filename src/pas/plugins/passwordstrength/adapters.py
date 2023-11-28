from plone.base.interfaces import IForcePasswordChange
from pas.plugins.passwordstrength.interfaces import IPasPluginsPasswordstrengthLayer, IPasswordResetRequest
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.component import adapter
from zope.interface import Interface
from plone import api
from zExceptions import Unauthorized
import transaction


@implementer(IForcePasswordChange)
@adapter(Interface, IPasPluginsPasswordstrengthLayer)
class ForcePasswordChange:
    def __init__(self, context, request) -> None:
        self.context = context
        self.request = request

    def __call__(self):
        request = self.request
        response = request.response
        member = api.user.get_current()        
        reset_tool = api.portal.get_tool("portal_password_reset")
        reset = reset_tool.requestReset(member.getId())
        # XXX: need to commit here to make sure the reset is saved
        transaction.commit()
        base_url = api.portal.get_navigation_root(self.context).absolute_url()
        response.redirect(f"{base_url}/passwordreset/{reset['randomstring']}", lock=1)
        alsoProvides(request, IPasswordResetRequest)
        # response.setBody("Password change required", is_error=1)
        # response.setStatus(401)
        # XXX: need to raise an exception here to make sure the user is logged out and
        #      redirected to the password reset page. Custom challenge is used for
        #      the redirect and reset authentication.
        raise Unauthorized("Password change required")
