class DriverOutdatedError(Exception):
    """
    Raise this error when Chrome has been updated and the chromedriver for Selenium no longer matches versions
    """
    def __init__(self, message="The chromedriver version does not match the version of Chrome installed"):
            self.message = message
            super().__init__(self.message)