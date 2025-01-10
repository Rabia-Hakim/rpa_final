# Set up the driver with the local GeckoDriver path
service = Service(driverfirfox_location)
driver = webdriver.Firefox(service=service, options=options)
