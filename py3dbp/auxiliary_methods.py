from decimal import Decimal


def getLimitNumberOfDecimals(number_of_decimals: int) -> Decimal:
    return Decimal("1.{}".format("0" * number_of_decimals))


def set2Decimal(value: float, number_of_decimals: int = 0) -> Decimal:
    """
    Decimal('1.41421356').quantize(Decimal('1.000')) -> Decimal('1.414')
    """
    return Decimal(value).quantize(getLimitNumberOfDecimals(number_of_decimals))
