"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface

class IPasPluginsPasswordstrengthLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPasswordResetRequest(Interface):
    """Marker interface for password reset request."""