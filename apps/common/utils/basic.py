import uuid
from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from urllib.parse import urlparse


def json_parameter_validation(json_data, required_params):
    """Check parameter is available in json or not
    parameter:
    ---------
        json_data: dict, required
            A dictionary that should be validate by pramas are available or not
        required_params: list, required
            Those list of params that must be available on json_data
    return:
    ------
        required_params: list
            If required parameter is not in json_data then return that parameter name othrewise None
    """
    missing_params = []
    for param in required_params:
        if json_data.get(param, None) is None:
            missing_params.append(param)
    return missing_params


def get_user_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_user_browser_details(request):
    return request.headers.get("User-Agent")


def random_hex_code(length: int = 8) -> str:
    """
    To create a new random hex code of dynamic length.

    :parameter
        length (int): set how many character of hex code will generate. Default is 8 character.

    :return
        random hex code with dynamic length.
    """
    return uuid.uuid4().hex[:length]


def fix_internal_decimal_places(decimal_value: Decimal) -> Decimal:
    """Decimal value with 6 decimal places. Use it for internal calculations

    Args:
        decimal_value (Decimal): decimal value to be fixed decimal places

    Returns:
        Decimal: fixed 6 decimal places
    """
    fixed_decimal_places = decimal_value.quantize(
        Decimal(".000000"), rounding=ROUND_DOWN
    )
    return fixed_decimal_places


def fix_external_decimal_places(decimal_value: Decimal) -> Decimal:
    """Decimal value with 2 decimal places. Use it for api/external output

    Args:
        decimal_value (Decimal): decimal value to be fixed decimal places

    Returns:
        Decimal: fixed 2 decimal places
    """
    fixed_decimal_places = decimal_value.quantize(Decimal(".00"), rounding=ROUND_DOWN)
    return fixed_decimal_places


def get_value_by_percentage(value: Decimal, percentage: Decimal) -> Decimal:
    """Calculate value percentage of the price

    Args:
        value (Decimal): decimal value from which percentage value will be calculated
        percentage (Decimal): decimal value of percentage

    Returns:
        Decimal: value percentage
    """
    percentage_value = (percentage / Decimal(100)) * value
    return percentage_value


def convert_str_date_format(
    input_date, input_format="%d-%m-%Y", expected_format="%Y-%m-%d"
):
    """
    Convert string date to expected format
    :param input_date: Date string that needs to be converted
    :param input_format: Input date format
    :param expected_format: Expected date format
    :return: Date string in expected format
    """

    converted_date = datetime.strptime(input_date, input_format).strftime(
        expected_format
    )
    return converted_date


def is_absolute_uri(uri):
    """
    :param uri: Uri as string
    Check a uri is absolute uri or not
    """
    return bool(urlparse(uri).netloc)


def build_media_url(url):
    media_url = f"/media/{url}"
    return media_url


def datetime_now(with_tz=False):
    if with_tz:
        return datetime.now().astimezone()
    return datetime.now()
