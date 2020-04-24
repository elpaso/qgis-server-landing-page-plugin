# Landing Page API plugin

def serverClassFactory(serverIface):
    from .landingpage import LandingPageApi
    return LandingPageApi(serverIface)

