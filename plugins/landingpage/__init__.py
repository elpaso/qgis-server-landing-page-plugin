# Landing Page API plugin

def serverClassFactory(serverIface):
    from .landingpage import LandingPageApiLoader
    return LandingPageApiLoader(serverIface)

