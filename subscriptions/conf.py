"""Functions for general package configuration."""
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings


class Currency():
    """Object to hold currency details and format them.

        Currency formatting follows the standards used by the
        locale module and formatting the number follows a similar
        process: https://docs.python.org/3/library/locale.html

        Keyword Arguments:
            currency_symbol (str): The symbol used for this currency.
            int_currency_symbol (str): The symbol used for this
                currency for international formatting.
            p_cs_precedes (bool): Whether the currency symbol precedes
                positive values.
            n_cs_precedes (bool): Whether the currency symbol precedes
                negative values.
            p_sep_by_space (bool): Whether the currency symbol is
                separated from positive values by a space.
            n_sep_by_space (bool): Whether the currency symbol is
                separated from negative values by a space.
            mon_decimal_point (str): The character used for decimal
                points.
            mon_thousands_sep (str): The character used for separating
                groups of numbers.
            mon_grouping (int): The number of digits per groups.
            frac_digits (int): The number of digits following the
                decimal place.
            int_frac_digits (int): The number of digits following the
                decimal place for international formatting.
            positive_sign (str): The symbol to use for the positive
                sign.
            negative_sign (str): The symbol to use for the negative
                sign.
            p_sign_posn (int): How the positive sign should be
                positioned relative to the currency symbol and value
                (see below).
            n_sign_posn (int): How the positive sign should be
                positioned relative to the currency symbol and value
                (see below).

        Sign Position (``sign_posn``):
            0: Currency and value are surrounded by parentheses.
            1: The sign should precede the value and currency symbol.
            2: The sign should follow the value and currency symbol.
            3: The sign should immediately precede the value.
            4: The sign should immediately follow the value.
    """
    def __init__(self, **kwargs):
        self.currency_symbol = kwargs.get('currency_symbol', '')
        self.int_curr_symbol = kwargs.get('int_curr_symbol', '')
        self.p_cs_precedes = kwargs.get('p_cs_precedes', True)
        self.n_cs_precedes = kwargs.get('n_cs_precedes', True)
        self.p_sep_by_space = kwargs.get('p_sep_by_space', False)
        self.n_sep_by_space = kwargs.get('n_sep_by_space', False)
        self.mon_decimal_point = kwargs.get('mon_decimal_point', '.')
        self.mon_thousands_sep = kwargs.get('mon_thousands_sep', '')
        self.mon_grouping = kwargs.get('mon_grouping', 3)
        self.frac_digits = kwargs.get('frac_digits', 2)
        self.int_frac_digits = kwargs.get('int_frac_digits', 2)
        self.positive_sign = kwargs.get('positive_sign', '')
        self.negative_sign = kwargs.get('negative_sign', '')
        self.p_sign_posn = kwargs.get('p_sign_posn', '')
        self.n_sign_posn = kwargs.get('n_sign_posn', '')

    def format_currency(self, value, international=False):
        """Returns the provided value in the proper currency format.

            Parameters:
                value (dec): The decimal to represent as a currency.
                international (bool): Whether this should follow
                    international formatting or not.

            Returns:
                str: The formatted currency value.
        """
        # Convert value to decimal for future operations
        value = Decimal(value)

        # Round to required number of digits:
        #   - uses ROUND_HALF_UP, to give the most intuitive result to a
        #     typical user
        #   - uses absolute value as negative signs will be applied later
        digits = self.int_frac_digits if international else self.frac_digits
        decimal_str = abs(value).quantize(
            Decimal(10) ** -digits, rounding=ROUND_HALF_UP,
        )

        # Split decimal into whole and fractions
        num_whole, num_frac = str(decimal_str).split('.')

        # Apply any grouping to the whole number component
        group_sep = self.mon_thousands_sep
        grouping = self.mon_grouping
        remaining = num_whole
        groups = []

        while remaining:
            groups.append(remaining[-grouping:])
            remaining = remaining[:-grouping]

        groups.reverse()
        grouped_num_whole = group_sep.join(groups)

        # Rejoin number parts with decimal separator
        decimal_point = self.mon_decimal_point
        formatted_number = '{}{}{}'.format(
            grouped_num_whole, decimal_point, num_frac
        )

        # '<' and '>' are used as markers of number start and end
        formatted_currency = '<{}>'.format(formatted_number)

        # Determine details of additional formatting
        if value < 0:
            precedes = self.n_cs_precedes
            separated = ' ' if self.n_sep_by_space else ''
            sign = self.negative_sign
            sign_position = self.n_sign_posn
        else:
            precedes = self.p_cs_precedes
            separated = ' ' if self.p_sep_by_space else ''
            sign = self.positive_sign
            sign_position = self.p_sign_posn

        # Place the currency symbol
        symbol = (
            self.int_curr_symbol if international else self.currency_symbol
        )

        if precedes:
            formatted_currency = '{}{}{}'.format(
                symbol, separated, formatted_currency
            )
        else:
            formatted_currency = '{}{}{}'.format(
                formatted_currency, separated, symbol
            )

        # Insert the proper sign for positive/negative values
        if sign_position == 0:
            formatted_currency = '({})'.format(formatted_currency)
        elif sign_position == 1:
            formatted_currency = '{}{}'.format(sign, formatted_currency)
        elif sign_position == 2:
            formatted_currency = '{}{}'.format(formatted_currency, sign)
        elif sign_position == 3:
            formatted_currency = formatted_currency.replace('<', sign)
        elif sign_position == 4:
            formatted_currency = formatted_currency.replace('>', sign)
        else:
            formatted_currency = '{}{}'.format(sign, formatted_currency)

        # Remove the placeholders for number start/end
        formatted_currency = (
            formatted_currency.replace('<', '').replace('>', '')
        )

        return formatted_currency

def compile_settings():
    """Compiles and validates all package settings and defaults.

        Provides basic checks to ensure required settings are declared
        and applies defaults for all missing settings.

        Returns:
            dict: All possible Django Flexible Subscriptions settings.
    """
    # ADMIN SETTINGS
    # -------------------------------------------------------------------------
    enable_admin = getattr(settings, 'DFS_ENABLE_ADMIN', False)
    # CURRENCY SETTINGS
    # -------------------------------------------------------------------------
    currency_locale = str(
        getattr(settings, 'DFS_CURRENCY_LOCALE', 'en_us')
    ).lower()

    # TEMPLATE SETTINGS
    # -------------------------------------------------------------------------
    base_template = getattr(
        settings, 'DFS_BASE_TEMPLATE', 'subscriptions/base.html'
    )

    return {
        'enable_admin': enable_admin,
        'currency_locale': currency_locale,
        'base_template': base_template,
    }


SETTINGS = compile_settings()

# Convenience values for sign positions
SIGN_PARANTHESES = 0
SIGN_PRECEDE_VALUE_SYMBOL = 1
SIGN_FOLLOW_VALUE_SYMBOL = 2
SIGN_PRECEDE_VALUE = 3
SIGN_FOLLOW_VALUE = 4

CURRENCY = {
    'en_ca': Currency(
        currency_symbol='$',
        int_curr_symbol='CAD',
        p_cs_precedes=True,
        n_cs_precedes=True,
        p_sep_by_space=False,
        n_sep_by_space=False,
        mon_decimal_point='.',
        mon_thousands_sep=',',
        mon_grouping=3,
        frac_digits=2,
        int_frac_digits=2,
        positive_sign='',
        negative_sign='-',
        p_sign_posn=SIGN_PRECEDE_VALUE,
        n_sign_posn=SIGN_PRECEDE_VALUE,
    ),
    'en_us': Currency(
        currency_symbol='$',
        int_curr_symbol='USD',
        p_cs_precedes=True,
        n_cs_precedes=True,
        p_sep_by_space=False,
        n_sep_by_space=False,
        mon_decimal_point='.',
        mon_thousands_sep=',',
        mon_grouping=3,
        frac_digits=2,
        int_frac_digits=2,
        positive_sign='',
        negative_sign='-',
        p_sign_posn=SIGN_PRECEDE_VALUE,
        n_sign_posn=SIGN_PARANTHESES,
    ),
    'fr_ca': Currency(
        currency_symbol='$',
        int_curr_symbol='CAD',
        p_cs_precedes=False,
        n_cs_precedes=False,
        p_sep_by_space=True,
        n_sep_by_space=True,
        mon_decimal_point=',',
        mon_thousands_sep='\xa0',
        mon_grouping=3,
        frac_digits=2,
        int_frac_digits=2,
        positive_sign='',
        negative_sign='-',
        p_sign_posn=SIGN_PRECEDE_VALUE_SYMBOL,
        n_sign_posn=SIGN_PARANTHESES,
    ),
}
