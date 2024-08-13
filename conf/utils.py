APPLICATION_NAME = "docman"
COMPANY_NAME = "docman"
COMPANY_EMAIL = "contact@docman.com"
COMPANY_PHONE = "+970-360-5788"
FAVICON_URL = "base/company/img/logo.png"
COMPANY_NAME_ICON_URL = "base/company/img/logo.png"
JS_VERSION = "1.00"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGIN_EXEMPT_URLS = [
    "reset/",
    "registration/",
    "account/activation/",
    "recover-password/",
    "api/*",
]
