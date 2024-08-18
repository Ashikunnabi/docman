class MetadataFieldType:
    TEXT = "text"
    INTEGER = "integer"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    IMAGE = "image"
    FILE = "file"
    HTML = "html"
    MARKDOWN = "markdown"
    COLOR = "color"
    COLOR_HEX = "color_hex"
    PASSWORD = "password"
    SECRET = "secret"
    PERCENTAGE = "percentage"
    RATING = "rating"
    COUNTRY = "country"
    LANGUAGE = "language"
    TIMEZONE = "timezone"
    CURRENCY_CODE = "currency_code"

    CHOICES = (
        (TEXT, "Text"),
        (INTEGER, "Integer"),
        (DECIMAL, "Decimal"),
        (BOOLEAN, "Boolean"),
        (DATE, "Date"),
        (DATETIME, "Datetime"),
        (TIME, "Time"),
        (URL, "URL"),
        (EMAIL, "Email"),
        (PHONE, "Phone"),
        (IMAGE, "Image"),
        (FILE, "File"),
        (HTML, "HTML"),
        (MARKDOWN, "Markdown"),
        (COLOR, "Color"),
        (COLOR_HEX, "Color (Hex)"),
        (PASSWORD, "Password"),
        (SECRET, "Secret"),
        (PERCENTAGE, "Percentage"),
        (RATING, "Rating"),
        (COUNTRY, "Country"),
        (LANGUAGE, "Language"),
        (TIMEZONE, "Timezone"),
        (CURRENCY_CODE, "Currency Code"),
    )
