import decimal
import re
import unicodedata

from django.core.validators import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.common.rest_utils.exceptions import BadRequestException
from rest_framework.exceptions import ValidationError as RestValidationError

from .utils.basic import is_absolute_uri


class BaseValidator(object):
    """This is the base validator, provides the validate method"""

    def __init__(self, *args, **kwargs):
        self.obj = kwargs["obj"]

    def validate(self):
        pass


class ScreenMethodValidator(BaseValidator):
    """This validators runs all 'screen_*' methods of the object"""

    def validate(self):
        screen_methods = self.obj.get_screen_methods()
        for method in screen_methods:
            result = method()
            if result:
                raise BadRequestException(result)


def remove_diacritics(text):
    """
    Returns a string with all diacritics (aka non-spacing marks) removed.
    For example "Héllô" will become "Hello".
    Useful for comparing strings in an accent-insensitive fashion.
    from: https://stackoverflow.com/questions/35783135/regex-match-a-character-and-all-its-diacritic-variations-aka-accent-insensiti/35783136
    """
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def validate_company_name(value):
    value = remove_diacritics(value)
    if not re.match("^[a-zA-Z0-9 ,.'\"\-/&+@!#$%^*()]{1,100}$", value):
        error_message = "Company name allows only alphanumeric characters, space, comma, apostrophe backslash and \-/&+@!#$%^*()."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_char_field(value):
    # if the string contains alphanumeric
    # and if the len of string is >= 3
    # and if the string match permitted sequence
    if (
        re.search(".*\w", value)
        and len(value) >= 3
        and re.match(r"$|^[\w )(/=#.-]+$", value)
    ):
        return value
    else:
        error_message = "Only alphanumeric characters, underscore, space, dot and hyphen are allowed. \
            Min 3 characters expected."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_initials(value):
    if not re.match("^[a-zA-Z .-]{1,12}$", value):
        error_message = 'Initial must be in correct format, valid characters are "a-zA-Z .-, maximum 12 characters".'
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_surname(value):
    value = remove_diacritics(value)
    if not re.match("^[a-zA-Z .'-]{1,50}$", value):
        error_message = "Surname allows only letter, space, dot and hyphen."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_last_name(value):
    value = remove_diacritics(value)
    if not re.match("^(?!.*[,,]{2})(?!.*[ ]{2})[a-zA-Z0-9 ,.'-]{1,95}$", value):
        # if not re.match("^[a-zA-Z0-9 ,.'-]{2,95}$", value):
        error_message = (
            "Last name allows only alphanumeric characters, space, apostrophe, dot and hyphen minimum 2 maximum 95 characters."
            " Two consicutive spaces or comma not allowed."
        )
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_last_name_for_business_user(coc_number, last_name):
    value = remove_diacritics(last_name)
    if coc_number:
        if not re.match("^(?!.*[,,]{2})(?!.*[ ]{2})[a-zA-Z0-9 ,.'-]{1,95}$", value):
            # if not re.match("^[a-zA-Z0-9 ,.'-]{2,95}$", value):
            error_message = (
                "Last name allows only alphanumeric characters, space, apostrophe, dot and hyphen minimum 2 maximum 95 characters."
                " Two consicutive spaces or comma not allowed."
            )
            error = {
                "last_name": {
                    "error": error_message,
                    "message": error_message,
                }
            }
            # TODO: Move to custom exception class
            raise RestValidationError(error)
    else:
        if not re.match("^(?!.*[,,]{2})(?!.*[ ]{2})[a-zA-Z ,.'-]{1,95}$", value):
            # if not re.match("^[a-zA-Z ,.'-]{2,95}$", value):
            error_message = (
                "Last name allows only letter, space, apostrophe, dot and hyphen minimum 2 maximum 95 characters."
                " Two consicutive space or comma not allowed."
            )
            error = {
                "last_name": {
                    "error": error_message,
                    "message": error_message,
                }
            }
            # TODO: Move to custom exception class
            raise RestValidationError(error)


def validate_birth_name(value):
    value = remove_diacritics(value)
    if not re.match("^[a-zA-Z ,.'-]{1,50}$", value):
        error_message = (
            "Birth name allows only letter, space, comma, apostrophe, dot and hyphen."
        )
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_mobile_number(value):
    regex = "^(((\+[ -\.]?31|0|00([ -\.]?)31)[ -\.]?6){1}[ -\.]?[1-9]{1}(?:([ -\.]?[0-9])){7})$|^(((0|\+31)97){1}?[0-9]{9})$"
    if not re.match(regex, value):
        error_message = "Mobiele nummer start met 06 of 316 ."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_phone_number(value):
    """
    This validation is for mobile and fixed
    :param value:
    :return:
    """
    regex = "^(\+31|0031|0)(([2357]{1}|[14](?!4)|[8](?=[578]))(?:([ -]?[0-9])){8}|[6]([ -]?)[1-9]{1}(?:([ -]?[0-9])){7}|(97){1}[0-8]{1}(?:([ -]?[0-9])){8})$"
    if not re.match(regex, value):
        error_message = "Phone number must be 10 digit including prefix 0."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_back_account_last_four_digit(value):
    error_code = "Invalid Last Digits"
    error_message = "Bank account last digits should be integers"

    if re.match("^[0-9]+$", value) and len(value) == 4:
        return value
    return RestValidationError({"error": error_code, "message": error_message})


def validate_past_date_or_empty(value):
    if not value:
        return

    if value > timezone.now().date():
        error_message = "Datum moet in de verleden liggen."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_house_number_with_max_value(value):
    max_value = 100000
    if isinstance(value, int) and value > 0 and value <= max_value:
        return

    error_message = "Number should not be larger than {}".format(max_value)
    # TODO: Move to custom exception class
    raise RestValidationError({"error": error_message, "message": error_message})


def validate_house_number_extension(value):
    if not re.match("^[a-zA-Z0-9 .\-]{1,5}$", value):
        error_message = "House number extension allows only alphanumeric characters, space, backslash, dot and hyphen."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_street(value):
    value = remove_diacritics(value)
    if not re.match("^[a-zA-Z0-9 ,.'\-&()]{1,50}$", value):
        error_message = (
            "Street allows only alphanumeric characters, space and ,.'\-&()."
        )
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_city(value):
    value = remove_diacritics(value)
    if not re.match(r"^[a-zA-Z0-9 ,.'\-()]{1,50}$", value):
        error_message = "City allows only alphanumeric characters, space, comma, apostrophe, dot and hyphen."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_zip_code(value):
    valid_zip_code = "1234 SD, 4700 se, 3235 ER"
    if not re.match(r"^[0-9]{4}\s?[A-Za-z]{2}$", value):
        error_message = (
            "Zip code must contains 4 digits exactly followed by 2 capital letters exactly ex: {}".format(
                valid_zip_code
            ),
        )
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_birthday(birthday):
    today = timezone.datetime.today()
    age = (
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )

    if age < 18 or age > 115:
        error_message = "Minimale leeftijd is 18 jaar, vul juiste geboortedatum in."
        # TODO: Move to custom exception class
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_imei_number(value):
    """
    This screen method validates IMEI number pattern.
    :return:
    """
    imei_number = value

    if imei_number is not None and imei_number != "":
        imei_number_digits_array = list(imei_number)

        if len(imei_number_digits_array) != 15:
            error_message = "Invalid IMEI. Need Exactly 15 numeric digits."
            # TODO: Move to custom exception class
            raise RestValidationError(
                {"error": error_message, "message": error_message}
            )

        for char in imei_number_digits_array:
            try:
                digit = int(char)
            except ValueError:
                error_message = "Invalid IMEI. Need only numeric digits."
                # TODO: Move to custom exception class
                raise RestValidationError(
                    {"error": error_message, "message": error_message}
                )

        last_digit = imei_number_digits_array.pop()

        checksum = 0
        for digit_index, digit in enumerate(imei_number_digits_array):
            if digit_index % 2 == 0:
                checksum += int(digit)
            else:
                even_digit_double = int(digit) * 2
                double_product_array = list(str(even_digit_double))

                for single_digit in double_product_array:
                    checksum += int(single_digit)

        if (checksum * 9) % 10 != int(last_digit):
            error_message = "Invalid IMEI."
            # TODO: Move to custom exception class
            raise RestValidationError(
                {"error": error_message, "message": error_message}
            )


def validate_percentage(value):
    if value < decimal.Decimal("0.00"):
        error_message = _("Percentage value must be greater than or equal to 0")
    elif value > decimal.Decimal("100.00"):
        error_message = _("Percentage value must be less than or equal to 100")
    else:
        return value
    raise RestValidationError({"error": error_message, "message": error_message})


def validate_discount_price(value):
    if value < decimal.Decimal("0.00"):
        error_message = _("Het kortingsbedrag mag de totale prijs niet overschrijden.")
    elif value > decimal.Decimal("100.00"):
        error_message = _("Het kortingsbedrag mag de totale prijs niet overschrijden.")
    else:
        return value
    raise RestValidationError({"error": error_message, "message": error_message})


def validate_cas_ids(value):
    if (
        re.search(".*\w", value)
        and len(value) >= 3
        and re.match(r"$|^[\w )(/=#.,-]+$", value)
    ):
        return value
    else:
        error_message = "Only alphanumeric characters, underscore, space, comma, dot and hyphen are allowed. \
            Min 3 characters expected."
        raise RestValidationError({"error": error_message, "message": error_message})


def validate_url(value):
    if not is_absolute_uri(value):
        raise RestValidationError(
            {"error": "IN_VALID_URL", "message": "Please provide a valid url"}
        )


def validate_purchase_price_ex_vat(value):
    if value < decimal.Decimal("0.00"):
        error_message = _("Purchase price must be greater than or equal to 0")
    else:
        return value
    raise RestValidationError({"error": error_message, "message": error_message})


def validate_sales_price_ex_vat(value):
    if value < decimal.Decimal("0.00"):
        error_message = _("Sales price must be greater than or equal to 0")
    else:
        return value
    raise RestValidationError({"error": error_message, "message": error_message})
