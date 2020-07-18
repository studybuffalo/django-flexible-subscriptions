"""Module to handle details involving currency formating."""
from decimal import Decimal, ROUND_HALF_UP


# Convenience values for sign positions
SIGN_PARANTHESES = 0
SIGN_PRECEDE_VALUE_SYMBOL = 1
SIGN_FOLLOW_VALUE_SYMBOL = 2
SIGN_PRECEDE_VALUE = 3
SIGN_FOLLOW_VALUE = 4

CURRENCY = {
    'de_de': {
        'currency_symbol': '€',
        'int_curr_symbol': 'EUR',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': ',',
        'mon_thousands_sep': '.',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE_SYMBOL,
        'n_sign_posn': SIGN_PARANTHESES,
    },
    'en_au': {
        'currency_symbol': '$',
        'int_curr_symbol': 'AUD',
        'p_cs_precedes': True,
        'n_cs_precedes': True,
        'p_sep_by_space': False,
        'n_sep_by_space': False,
        'mon_decimal_point': '.',
        'mon_thousands_sep': ',',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PRECEDE_VALUE_SYMBOL,
    },
    'en_ca': {
        'currency_symbol': '$',
        'int_curr_symbol': 'CAD',
        'p_cs_precedes': True,
        'n_cs_precedes': True,
        'p_sep_by_space': False,
        'n_sep_by_space': False,
        'mon_decimal_point': '.',
        'mon_thousands_sep': ',',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PRECEDE_VALUE,
    },
    'en_us': {
        'currency_symbol': '$',
        'int_curr_symbol': 'USD',
        'p_cs_precedes': True,
        'n_cs_precedes': True,
        'p_sep_by_space': False,
        'n_sep_by_space': False,
        'mon_decimal_point': '.',
        'mon_thousands_sep': ',',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PARANTHESES,
    },
    'fa_ir': {
        'currency_symbol': '﷼',
        'int_curr_symbol': 'IRR',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': '.',
        'mon_thousands_sep': ',',
        'mon_grouping': 3,
        'frac_digits': 0,
        'int_frac_digits': 0,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE_SYMBOL,
        'n_sign_posn': SIGN_PRECEDE_VALUE_SYMBOL
    },
    'fr_ca': {
        'currency_symbol': '$',
        'int_curr_symbol': 'CAD',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': ',',
        'mon_thousands_sep': '\xa0',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE_SYMBOL,
        'n_sign_posn': SIGN_PARANTHESES,
    },
    'pl_pl': {
        'currency_symbol': 'zł',
        'int_curr_symbol': 'PLN',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': ',',
        'mon_thousands_sep': '.',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE_SYMBOL,
        'n_sign_posn': SIGN_PARANTHESES,
    },
    'fr_fr': {
        'currency_symbol': '€',
        'int_curr_symbol': 'EUR',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': ',',
        'mon_thousands_sep': '.',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PRECEDE_VALUE,
    },
    'fr_ch': {
        'currency_symbol': 'CHF',
        'int_curr_symbol': 'CHF',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': '.',
        'mon_thousands_sep': "'",
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PRECEDE_VALUE,
    },
    'it_it': {
        'currency_symbol': '€',
        'int_curr_symbol': 'EUR',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': ',',
        'mon_thousands_sep': ".",
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PRECEDE_VALUE,
    },
    'pt_br': {
        'currency_symbol': 'R$',
        'int_curr_symbol': 'BRL',
        'p_cs_precedes': False,
        'n_cs_precedes': False,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'mon_decimal_point': ',',
        'mon_thousands_sep': ".",
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PRECEDE_VALUE,
    },
    'en_in': {
        'currency_symbol': '₹',
        'int_curr_symbol': 'INR',
        'p_cs_precedes': True,
        'n_cs_precedes': True,
        'p_sep_by_space': False,
        'n_sep_by_space': False,
        'mon_decimal_point': '.',
        'mon_thousands_sep': ',',
        'mon_grouping': 3,
        'frac_digits': 2,
        'int_frac_digits': 2,
        'positive_sign': '',
        'negative_sign': '-',
        'p_sign_posn': SIGN_PRECEDE_VALUE,
        'n_sign_posn': SIGN_PARANTHESES,
    },
}


class Currency():
    """Defines and outputs formatted currency strings.

        Parameters:
            currency_locale (str or dict): a currency locale string or
                a dictionary defining custom currency formating
                conventions.
    """
    def __init__(self, currency_locale):
        self.international = False
        self.locale = None
        self.conventions = self._assign_currency_conventions(currency_locale)

    def _assign_currency_conventions(self, currency_locale):
        """Assigns currency conventions based on specified locale.

            If a dictionary is provided, the user is
            manually specifying the formating conventions. If a string
            is provided, the user is using a predefined currency locale.

            Parameters:
                currency_locale (str or dict): the currency locale to
                    use for formating conventions.

            Returns:
                dict: dictionary of formating conventions.
        """
        # If dictionary is passed, user is specifying their own values
        if isinstance(currency_locale, dict):
            self.locale = 'custom'

            return {
                'currency_symbol': currency_locale.get('currency_symbol', ''),
                'int_curr_symbol': currency_locale.get('int_curr_symbol', ''),
                'p_cs_precedes': currency_locale.get('p_cs_precedes', True),
                'n_cs_precedes': currency_locale.get('n_cs_precedes', True),
                'p_sep_by_space': currency_locale.get('p_sep_by_space', False),
                'n_sep_by_space': currency_locale.get('n_sep_by_space', False),
                'mon_decimal_point': currency_locale.get('mon_decimal_point', '.'),
                'mon_thousands_sep': currency_locale.get('mon_thousands_sep', ''),
                'mon_grouping': currency_locale.get('mon_grouping', 3),
                'frac_digits': currency_locale.get('frac_digits', 2),
                'int_frac_digits': currency_locale.get('int_frac_digits', 2),
                'positive_sign': currency_locale.get('positive_sign', ''),
                'negative_sign': currency_locale.get('negative_sign', ''),
                'p_sign_posn': currency_locale.get('p_sign_posn', ''),
                'n_sign_posn': currency_locale.get('n_sign_posn', ''),
            }

        # Otherwise, they have specified an existing locale
        self.locale = currency_locale.lower()

        return CURRENCY[self.locale]

    def _determine_frac_digits(self):
        """Determines number of fractional digits to round to.

            Returns:
                int: the number of fractional digits for currency display.
        """
        if self.international:
            return self.conventions['int_frac_digits']

        return self.conventions['frac_digits']

    def _split_value(self, value):
        """Splits provided value into whole and fractional parts.

            Parameters:
                value (dec): the value to split into components.

            Returns:
                tuple: the whole number and fractional number
                    components as strings.
        """
        # Determine number of fractional digits to use for this value
        digits = self._determine_frac_digits()

        # Round to required number of digits:
        #   - uses ROUND_HALF_UP, to give the most intuitive result to a
        #     typical user
        #   - uses absolute value as negative signs will be applied later
        decimal_str = abs(value).quantize(
            Decimal(10) ** -digits, rounding=ROUND_HALF_UP,
        )

        # Split decimal into whole and fractions
        try:
            num_whole, num_frac = str(decimal_str).split('.')
        except ValueError:
            num_whole, num_frac = str(decimal_str), ''

        return num_whole, num_frac

    def _group_whole_num(self, num_whole):
        """Formats whole number into appropriate groups.

            Parameters:
                num_whole (str): the whole number portion of the value.

            Returns:
                str: the whole number with appropriate grouping applied.
        """
        remaining = num_whole
        groups = []

        while remaining:
            groups.append(remaining[-self.conventions['mon_grouping']:])
            remaining = remaining[:-self.conventions['mon_grouping']]

        groups.reverse()
        grouped_num_whole = self.conventions['mon_thousands_sep'].join(groups)

        return grouped_num_whole

    def _format_value(self, num_whole, num_frac):
        """Returns formatted value with appropriate decimal seperator.

            Parameters:
                num_whole (str): the whole number portion of the value.
                num_frac (str): the fractional portion of the value.

            Returns:
                str: combined value, separated by the decimal separator.
        """
        frac_digits = self._determine_frac_digits()

        # Determines decimal separator (only required if currency uses fractions)
        if frac_digits > 0:
            dec_separator = self.conventions['mon_decimal_point']
        else:
            dec_separator = ''

        # Assemble and return the formatted value
        return '{}{}{}'.format(
            num_whole, dec_separator, num_frac
        )

    def _determine_symbol_details(self, negative_value):
        """Determines positioning of required symbols.

            Parameters:
                negative_value (bool): whether this is a negative
                    value or not.

            Returns:
                obj: Currency symbol and positioning details.
        """
        # Determine which symbol to use
        if self.international:
            symbol = self.conventions['int_curr_symbol']
        else:
            symbol = self.conventions['currency_symbol']

        # If value less than zero, assign negative symbol details
        if negative_value:
            return {
                'symbol': symbol,
                'precedes': self.conventions['n_cs_precedes'],
                'separated': ' ' if self.conventions['n_sep_by_space'] else '',
                'sign': self.conventions['negative_sign'],
                'sign_position': self.conventions['n_sign_posn'],
            }

        # Otherwise return positive symbol details
        return {
            'symbol': symbol,
            'precedes': self.conventions['p_cs_precedes'],
            'separated': ' ' if self.conventions['p_sep_by_space'] else '',
            'sign': self.conventions['positive_sign'],
            'sign_position': self.conventions['p_sign_posn'],
        }

    def add_symbols(self, value, negative_value):
        """Adds currency and positive/negative symbols to the value.

            Parameters:
                value (str): the formatted value to add
                    symbols to.
                negative_value (bool): whether this is a negative
                    value or not.

            Returns:
                str: the final value formatted as a currency value.
        """
        # '<' and '>' are used as markers of number start and end
        placeholder_value = '<{}>'.format(value)

        # Determine details of additional formatting
        symbol = self._determine_symbol_details(negative_value)

        if symbol['precedes']:
            placeholder_value = '{}{}{}'.format(
                symbol['symbol'], symbol['separated'], placeholder_value
            )
        else:
            placeholder_value = '{}{}{}'.format(
                placeholder_value, symbol['separated'], symbol['symbol']
            )

        # Insert the proper sign for positive/negative values
        if symbol['sign_position'] == 0:
            placeholder_value = '({})'.format(placeholder_value)
        elif symbol['sign_position'] == 1:
            placeholder_value = '{}{}'.format(symbol['sign'], placeholder_value)
        elif symbol['sign_position'] == 2:
            placeholder_value = '{}{}'.format(placeholder_value, symbol['sign'])
        elif symbol['sign_position'] == 3:
            placeholder_value = placeholder_value.replace('<', symbol['sign'])
        elif symbol['sign_position'] == 4:
            placeholder_value = placeholder_value.replace('>', symbol['sign'])
        else:
            placeholder_value = '{}{}'.format(symbol['sign'], placeholder_value)

        # Remove the placeholders for number start/end
        formatted_currency = (
            placeholder_value.replace('<', '').replace('>', '')
        )

        return formatted_currency

    def format_currency(self, value, international=False):
        """Returns the provided value in the proper currency format.

            Parameters:
                value (dec): The decimal to represent as a currency.
                international (bool): Whether this should follow
                    international formatting or not.

            Returns:
                str: The formatted currency value.
        """
        # Assign international status for currency format
        self.international = international

        # Convert value to decimal for future operations
        value = Decimal(value)

        # Split value into whole and fractional parts
        num_whole, num_frac = self._split_value(value)

        # Apply any grouping to the whole number component
        grouped_num_whole = self._group_whole_num(num_whole)

        # Rejoin whole and fractional numbers with decimal separator
        formatted_value = self._format_value(grouped_num_whole, num_frac)

        # Add currency and positive/negative symbols
        formatted_currency = self.add_symbols(formatted_value, bool(value < 0))

        return formatted_currency
