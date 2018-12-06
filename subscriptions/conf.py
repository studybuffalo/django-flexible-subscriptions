"""Functions for general package configuration."""
from decimal import Decimal

from django.conf import settings


class Currency():
    """Object to hold currency details and format them.

        Currency formatting follows the standards used by the
        locale module and formatting the number follows a similar
        process: https://docs.python.org/3/library/locale.html

        Keyword Arguments:
            currency_symbol (str): The symbol used for this currency
                (**default:** `$`)
            int_currency_symbol (str):
            p_cs_precedes (bool):
            n_cs_precedes (bool):
            p_sep_by_space (bool):
            n_sep_by_space (bool):
            mon_decimal_point (str):
            mon_thousands_sep (str):
            mon_grouping (int):
            frac_digits (int):
            int_frac_digits (int):
            positive_sign (str):
            negative_sign (str):
            p_sign_posn (int):
            n_sign_posn (int):
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
        # Convert value to decimal and round to proper number of digits
        digits = self.int_frac_digits if international else self.frac_digits
        value = Decimal(value).quantize(Decimal(10) ** -digits)

        # Split decimal into whole and fractions
        num_whole, num_frac = str(value).split('.')

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
    """Compiles and validates all package settings and deaults.

        Provides basic checks to ensure required settings are declared
        and applies defaults for all missing settings.

        Returns:
            dict: All possible Django Flexible Subscriptions settings.
    """
    # ADMIN SETTINGS
    # -------------------------------------------------------------------------
    enable_admin = getattr(
        settings, 'SUBSCRIPTIONS_ENABLE_ADMIN', False
    )
    # CURRENCY SETTINGS
    # -------------------------------------------------------------------------
    currency_locale = str(getattr(
        settings, 'SUBSCRIPTIONS_CURRENCY_LOCALE', 'en_us'
    )).lower()

    return {
        'enable_admin': enable_admin,
        'currency_locale': currency_locale,
    }


SETTINGS = compile_settings()

CURRENCY = {
    'en_ca': Currency(
        currency_symbol='$',
        int_curr_symbol='CAD',
        cs_precedes=True,
        cs_sep_by_space=False,
        mon_decimal_point='.',
        mon_thousands_sep=',',
        mon_grouping=3,
        frac_digits=2,
        int_frac_digits=2,
        p_sign_posn=3,
        n_sign_posn=3,
    ),
    'en_us': Currency(
        currency_symbol='$',
        int_curr_symbol='USD',
        cs_precedes=True,
        cs_sep_by_space=False,
        mon_decimal_point='.',
        mon_thousands_sep=',',
        mon_grouping=3,
        frac_digits=2,
        int_frac_digits=2,
        p_sign_posn=3,
        n_sign_posn=0,
    ),
    'fr_ca': Currency(
        currency_symbol='$',
        int_curr_symbol='CAD',
        cs_precedes=True,
        cs_sep_by_space=False,
        mon_decimal_point=',',
        mon_thousands_sep='\xa0',
        mon_grouping=3,
        frac_digits=2,
        int_frac_digits=2,
        p_sign_posn=1,
        n_sign_posn=0,
    ),
}
