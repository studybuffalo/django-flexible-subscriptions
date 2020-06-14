"""Tests for the currency module."""
# pylint: disable=protected-access, too-many-lines
from decimal import Decimal

from subscriptions import currency


def test__currency__init__defaults():
    """Confirms defaults of __init__."""
    test_currency = currency.Currency({})

    assert test_currency.international is False
    assert isinstance(test_currency.locale, str)
    assert isinstance(test_currency.conventions, dict)


def test__currency__assign_currency_conventions__dict():
    """Tests handling when dictionary is provided as currency_locale."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': 5,
        'n_sep_by_space': 6,
        'mon_decimal_point': 7,
        'mon_thousands_sep': 8,
        'mon_grouping': 9,
        'frac_digits': 10,
        'int_frac_digits': 11,
        'positive_sign': 12,
        'negative_sign': 13,
        'p_sign_posn': 14,
        'n_sign_posn': 15,
    }
    test_currency = currency.Currency(conventions)
    output_conventions = test_currency._assign_currency_conventions(conventions)

    assert test_currency.locale == 'custom'
    assert 'currency_symbol' in output_conventions
    assert 'int_curr_symbol' in output_conventions
    assert 'p_cs_precedes' in output_conventions
    assert 'n_cs_precedes' in output_conventions
    assert 'p_sep_by_space' in output_conventions
    assert 'n_sep_by_space' in output_conventions
    assert 'mon_decimal_point' in output_conventions
    assert 'mon_thousands_sep' in output_conventions
    assert 'mon_grouping' in output_conventions
    assert 'frac_digits' in output_conventions
    assert 'int_frac_digits' in output_conventions
    assert 'positive_sign' in output_conventions
    assert 'negative_sign' in output_conventions
    assert 'p_sign_posn' in output_conventions
    assert 'n_sign_posn' in output_conventions
    assert output_conventions['currency_symbol'] == 1
    assert output_conventions['int_curr_symbol'] == 2
    assert output_conventions['p_cs_precedes'] == 3
    assert output_conventions['n_cs_precedes'] == 4
    assert output_conventions['p_sep_by_space'] == 5
    assert output_conventions['n_sep_by_space'] == 6
    assert output_conventions['mon_decimal_point'] == 7
    assert output_conventions['mon_thousands_sep'] == 8
    assert output_conventions['mon_grouping'] == 9
    assert output_conventions['frac_digits'] == 10
    assert output_conventions['int_frac_digits'] == 11
    assert output_conventions['positive_sign'] == 12
    assert output_conventions['negative_sign'] == 13
    assert output_conventions['p_sign_posn'] == 14
    assert output_conventions['n_sign_posn'] == 15


def test__currency__assign_currency_conventions__dict_defaults():
    """Confirms default values when dictionary provided."""
    test_currency = currency.Currency({})
    conventions = test_currency._assign_currency_conventions({})

    assert conventions['currency_symbol'] == ''
    assert conventions['int_curr_symbol'] == ''
    assert conventions['p_cs_precedes'] is True
    assert conventions['n_cs_precedes'] is True
    assert conventions['p_sep_by_space'] is False
    assert conventions['n_sep_by_space'] is False
    assert conventions['mon_decimal_point'] == '.'
    assert conventions['mon_thousands_sep'] == ''
    assert conventions['mon_grouping'] == 3
    assert conventions['frac_digits'] == 2
    assert conventions['int_frac_digits'] == 2
    assert conventions['positive_sign'] == ''
    assert conventions['negative_sign'] == ''
    assert conventions['p_sign_posn'] == ''
    assert conventions['n_sign_posn'] == ''


def test__currency__assign_currency_conventions__str():
    """Confirms value when string currency_locale provided."""
    test_currency = currency.Currency('en_us')
    conventions = test_currency._assign_currency_conventions('en_us')

    assert test_currency.locale == 'en_us'
    assert conventions == currency.CURRENCY['en_us']


def test__currency__determine_frac_digits__local():
    """Confirms expected locale value is returned."""
    conventions = {'frac_digits': 1, 'int_frac_digits': 2}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    frac_digits = test_currency._determine_frac_digits()

    assert frac_digits == 1


def test__currency__determine_frac_digits__international():
    """Confirms expected international value is returned."""
    conventions = {'frac_digits': 1, 'int_frac_digits': 2}
    test_currency = currency.Currency(conventions)
    test_currency.international = True

    frac_digits = test_currency._determine_frac_digits()

    assert frac_digits == 2


def test__currency__split_value__no_frac_digits_whole_number():
    """Confirms output for no frac_digits and whole number provided."""
    conventions = {'frac_digits': 0}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    whole, frac = test_currency._split_value(Decimal('4'))

    assert whole == '4'
    assert frac == ''


def test__currency__split_value__frac_digits_whole_number():
    """Confirms output for no frac_digits and whole number provided."""
    conventions = {'frac_digits': 1}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    whole, frac = test_currency._split_value(Decimal('4'))

    assert whole == '4'
    assert frac == '0'


def test__currency__split_value__no_frac_digits_with_frac_round_down():
    """Confirms output for frac_digits and decimal provided to round down."""
    conventions = {'frac_digits': 0}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    whole, frac = test_currency._split_value(Decimal('4.3'))

    assert whole == '4'
    assert frac == ''


def test__currency__split_value__no_frac_digits_with_frac_round_up():
    """Confirms output for frac_digits and decimal provided to round up."""
    conventions = {'frac_digits': 0}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    whole, frac = test_currency._split_value(Decimal('4.6'))

    assert whole == '5'
    assert frac == ''


def test__currency__split_value__frac_digits_with_frac_round_down():
    """Confirms output for frac_digits and decimal provided."""
    conventions = {'frac_digits': 1}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    whole, frac = test_currency._split_value(Decimal('4.33'))

    assert whole == '4'
    assert frac == '3'


def test__currency__split_value__frac_digits_with_frac_round_up():
    """Confirms output for frac_digits and decimal provided."""
    conventions = {'frac_digits': 1}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    whole, frac = test_currency._split_value(Decimal('4.36'))

    assert whole == '4'
    assert frac == '4'


def test__currency__group_whole_num__zero_grouping():
    """Confirms output with a zero grouping."""
    conventions = {'mon_grouping': 0, 'mon_thousands_sep': '*'}
    test_currency = currency.Currency(conventions)

    grouped_whole = test_currency._group_whole_num('123456')

    assert grouped_whole == '123456'


def test__currency__group_whole_num__one_grouping():
    """Confirms output with a grouping of 1."""
    conventions = {'mon_grouping': 1, 'mon_thousands_sep': '*'}
    test_currency = currency.Currency(conventions)

    grouped_whole = test_currency._group_whole_num('123456')

    assert grouped_whole == '1*2*3*4*5*6'


def test__currency__group_whole_num__three_grouping():
    """Confirms output with a grouping of 1."""
    conventions = {'mon_grouping': 3, 'mon_thousands_sep': '*'}
    test_currency = currency.Currency(conventions)

    assert test_currency._group_whole_num('12') == '12'
    assert test_currency._group_whole_num('123') == '123'
    assert test_currency._group_whole_num('1234') == '1*234'
    assert test_currency._group_whole_num('12345') == '12*345'
    assert test_currency._group_whole_num('123456') == '123*456'


def test__currency__format_value__whole_num_with_frac_digits():
    """Tests formatting with a whole number and frac_digits."""
    conventions = {'frac_digits': 1, 'mon_decimal_point': '*'}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_value = test_currency._format_value('1', '')

    assert formatted_value == '1*'


def test__currency__format_value__whole_num_without_frac_digits():
    """Tests formatting with a whole number and no frac_digits."""
    conventions = {'frac_digits': 0, 'mon_decimal_point': '*'}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_value = test_currency._format_value('1', '')

    assert formatted_value == '1'


def test__currency__format_value__fractional_with_frac_digits():
    """Tests formatting with a whole number and frac_digits."""
    conventions = {'frac_digits': 1, 'mon_decimal_point': '*'}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_value = test_currency._format_value('1', '2')

    assert formatted_value == '1*2'


def test__currency__format_value__fractional_without_frac_digits():
    """Tests formatting with a whole number and no frac_digits."""
    conventions = {'frac_digits': 0, 'mon_decimal_point': '*'}
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_value = test_currency._format_value('1', '2')

    assert formatted_value == '12'


def test__currency__determine_symbol_details__local_positive():
    """Confirms output for locale positive value."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'positive_sign': 5,
        'negative_sign': 6,
        'p_sign_posn': 7,
        'n_sign_posn': 8,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    details = test_currency._determine_symbol_details(False)

    assert details['symbol'] == 1
    assert details['precedes'] == 3
    assert details['separated'] == ' '
    assert details['sign'] == 5
    assert details['sign_position'] == 7


def test__currency__determine_symbol_details__local_negative():
    """Confirms output for locale negative value."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'positive_sign': 5,
        'negative_sign': 6,
        'p_sign_posn': 7,
        'n_sign_posn': 8,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    details = test_currency._determine_symbol_details(True)

    assert details['symbol'] == 1
    assert details['precedes'] == 4
    assert details['separated'] == ' '
    assert details['sign'] == 6
    assert details['sign_position'] == 8


def test__currency__determine_symbol_details__international_positive():
    """Confirms output for locale positive value."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'positive_sign': 5,
        'negative_sign': 6,
        'p_sign_posn': 7,
        'n_sign_posn': 8,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = True

    details = test_currency._determine_symbol_details(False)

    assert details['symbol'] == 2
    assert details['precedes'] == 3
    assert details['separated'] == ' '
    assert details['sign'] == 5
    assert details['sign_position'] == 7


def test__currency__determine_symbol_details__international_negative():
    """Confirms output for locale negative value."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': True,
        'n_sep_by_space': True,
        'positive_sign': 5,
        'negative_sign': 6,
        'p_sign_posn': 7,
        'n_sign_posn': 8,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = True

    details = test_currency._determine_symbol_details(True)

    assert details['symbol'] == 2
    assert details['precedes'] == 4
    assert details['separated'] == ' '
    assert details['sign'] == 6
    assert details['sign_position'] == 8


def test__currency__determine_symbol_details__positive_not_sep_by_space():
    """Confirms proper output when p_sep_by_space is false."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': False,
        'n_sep_by_space': False,
        'positive_sign': 7,
        'negative_sign': 8,
        'p_sign_posn': 9,
        'n_sign_posn': 10,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    details = test_currency._determine_symbol_details(False)

    assert details['separated'] == ''


def test__currency__determine_symbol_details__negative_not_sep_by_space():
    """Confirms proper output when n_sep_by_space is false."""
    conventions = {
        'currency_symbol': 1,
        'int_curr_symbol': 2,
        'p_cs_precedes': 3,
        'n_cs_precedes': 4,
        'p_sep_by_space': False,
        'n_sep_by_space': False,
        'positive_sign': 7,
        'negative_sign': 8,
        'p_sign_posn': 9,
        'n_sign_posn': 10,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    details = test_currency._determine_symbol_details(True)

    assert details['separated'] == ''


def test__currency__add_symbols__precedes__position_0():
    """Tests currency symbol precedes and sign position 0."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 0,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '(! 1.1)'


def test__currency__add_symbols__precedes__position_1():
    """Tests currency symbol precedes and sign position 1."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 1,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '@! 1.1'


def test__currency__add_symbols__precedes__position_2():
    """Tests currency symbol precedes and sign position 2."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 2,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '! 1.1@'


def test__currency__add_symbols__precedes__position_3():
    """Tests currency symbol precedes and sign position 3."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 3,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '! @1.1'


def test__currency__add_symbols__precedes__position_4():
    """Tests currency symbol precedes and sign position 4."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 4,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '! 1.1@'


def test__currency__add_symbols__precedes__position_other():
    """Tests currency symbol precedes & fallback sign position."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 5,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '@! 1.1'


def test__currency__add_symbols__follows__position_0():
    """Tests currency symbol precedes and sign position 0."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 0,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '(1.1 !)'


def test__currency__add_symbols__follows__position_1():
    """Tests currency symbol follows and sign position 1."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 1,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '@1.1 !'


def test__currency__add_symbols__follows__position_2():
    """Tests currency symbol follows and sign position 2."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 2,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '1.1 !@'


def test__currency__add_symbols__follows__position_3():
    """Tests currency symbol follows and sign position 3."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 3,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '@1.1 !'


def test__currency__add_symbols__follows__position_4():
    """Tests currency symbol follows and sign position 4."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 4,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '1.1@ !'


def test__currency__add_symbols__follows__position_other():
    """Tests currency symbol follows & fallback sign position."""
    conventions = {
        'currency_symbol': '!',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
        'positive_sign': '@',
        'p_sign_posn': 5,
    }
    test_currency = currency.Currency(conventions)
    test_currency.international = False

    formatted_currency = test_currency.add_symbols('1.1', False)

    assert formatted_currency == '@1.1 !'


# UNIT TESTS TO CONFIRM ACTUAL OUTPUTS FROM FORMAT CURRENCY
# ----------------------------------------------------------------------------
def test__currency__format_currency__output__rounding_string():
    """Tests that rounding works as expected with string values."""
    test_currency = currency.Currency({})

    assert test_currency.format_currency('0.506') == '0.51'
    assert test_currency.format_currency('0.505') == '0.51'
    assert test_currency.format_currency('0.5049') == '0.50'
    assert test_currency.format_currency('0.005') == '0.01'
    assert test_currency.format_currency('0.0049') == '0.00'
    assert test_currency.format_currency('-0.0049') == '0.00'
    assert test_currency.format_currency('-0.005') == '0.01'


def test__currency__format_currency__output__rounding_decimal():
    """Tests that rounding works as expected with decimal values."""
    test_currency = currency.Currency({})

    assert test_currency.format_currency(Decimal('0.506')) == '0.51'
    assert test_currency.format_currency(Decimal('0.505')) == '0.51'
    assert test_currency.format_currency(Decimal('0.5049')) == '0.50'
    assert test_currency.format_currency(Decimal('0.005')) == '0.01'
    assert test_currency.format_currency(Decimal('0.0049')) == '0.00'
    assert test_currency.format_currency(Decimal('-0.0049')) == '0.00'
    assert test_currency.format_currency(Decimal('-0.005')) == '0.01'


def test__currency__format_currency__output__non_decimal_handling():
    """Tests that using a non-decimal currency will give correct result."""
    # Setup custom conventions for testing
    conventions = {'frac_digits': 0}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency(10) == '10'
    assert test_currency.format_currency('10') == '10'
    assert test_currency.format_currency('-100') == '100'
    assert test_currency.format_currency(-100) == '100'


def test__currency__format_currency__output__frac_digit_rounding():
    """Tests that digits are rounded as expected when truncated."""
    # Setup custom conventions for testing
    conventions = {'frac_digits':  0}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('0.6') == '1'
    assert test_currency.format_currency('0.5') == '1'
    assert test_currency.format_currency('0.49') == '0'
    assert test_currency.format_currency('-0.49') == '0'
    assert test_currency.format_currency('-1.005') == '1'
    assert test_currency.format_currency('-1.5') == '2'


def test__currency__format_currency__output__grouping_by_1():
    """Tests that grouping works properly for groups of 1."""
    # Setup custom conventions for testing
    conventions = {
        'mon_grouping': 1,
        'mon_thousands_sep': ',',
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '1.00'
    assert test_currency.format_currency('10.00') == '1,0.00'
    assert test_currency.format_currency('100.00') == '1,0,0.00'
    assert test_currency.format_currency('1000.00') == '1,0,0,0.00'


def test__currency__format_currency__output__grouping_by_3():
    """Tests that grouping works properly for groups of 3."""
    # Setup custom conventions for testing
    conventions = {
        'mon_grouping': 3,
        'mon_thousands_sep': ',',
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '1.00'
    assert test_currency.format_currency('10.00') == '10.00'
    assert test_currency.format_currency('100.00') == '100.00'
    assert test_currency.format_currency('1000.00') == '1,000.00'
    assert test_currency.format_currency('10000.00') == '10,000.00'
    assert test_currency.format_currency('100000.00') == '100,000.00'
    assert test_currency.format_currency('1000000.00') == '1,000,000.00'


def test__currency__format_currency__output__grouping_separator():
    """Tests that the grouping separator is properly applied."""
    # Setup custom conventions for testing
    conventions = {
        'mon_grouping': 3,
        'mon_thousands_sep': '*',
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1000000.00') == '1*000*000.00'


def test__currency__format_currency__output__symbol_precedes_positive_value():
    """Tests currency symbol is applied preceding a positive value."""
    # Setup custom conventions for testing
    conventions = {'currency_symbol': '$', 'p_cs_precedes': True}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '$1.00'


def test__currency__format_currency__output__symbol_precedes_negative_value():
    """Tests currency symbol is applied preceding a negative value."""
    # Setup custom conventions for testing
    conventions = {'currency_symbol': '$', 'n_cs_precedes': True}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '$1.00'


def test__currency__format_currency__output__symbol_follows_positive_value():
    """Tests currency symbol is applied following a positive value."""
    # Setup custom conventions for testing
    conventions = {'currency_symbol': '$', 'p_cs_precedes': False}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '1.00$'


def test__currency__format_currency___output__symbol_follows_negative_value():
    """Tests currency symbol is applied following a negative value."""
    # Setup custom conventions for testing
    conventions = {'currency_symbol': '$', 'n_cs_precedes': False}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '1.00$'


def test__currency__format_currency__output__symbol_precedes_with_space_positive():
    """Tests currency symbol is applied preceding positive value with space."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': True,
        'p_sep_by_space': True,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '$ 1.00'


def test__currency__format_currency__output__symbol_precedes_with_space_negative():
    """Tests currency symbol is applied preceding negative value with space."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': True,
        'n_sep_by_space': True,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '$ 1.00'


def test__currency__format_currency__output__symbol_follows_with_space_positive():
    """Tests currency symbol is applied following positive value with space."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'p_sep_by_space': True,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '1.00 $'


def test__currency__format_currency__output__symbol_follows_with_space_negative():
    """Tests currency symbol is applied following negative value with space."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'n_sep_by_space': True,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '1.00 $'


def test__currency__format_currency__output__symbol_international():
    """Tests that international currency symbol works properly."""
    # Setup custom conventions for testing
    conventions = {'int_curr_symbol': 'ABC'}

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00', international=True) == 'ABC1.00'


def test__currency__format_currency__output__sign_position_0_positive_preceding_cs():
    """Tests sign position 0, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'positive_sign': '+',
        'p_sign_posn': 0,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '($1.00)'


def test__currency__format_currency__output__sign_position_0_negative_preceding_cs():
    """Tests sign position 0, negative value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'negative_sign': '-',
        'n_sign_posn': 0,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '($1.00)'


def test__currency__format_currency__output__sign_position_0_positive_following_cs():
    """Tests sign position 0, positive value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'positive_sign': '+',
        'p_sign_posn': 0,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '(1.00$)'


def test__currency__format_currency__output__sign_position_0_negative_following_cs():
    """Tests sign position 0, negative value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'negative_sign': '-',
        'n_sign_posn': 0,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '(1.00$)'


def test__currency__format_currency__output__sign_position_1_positive_preceding_cs():
    """Tests sign position 1, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'positive_sign': '+',
        'p_sign_posn': 1,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '+$1.00'


def test__currency__format_currency__output__sign_position_1_negative_preceding_cs():
    """Tests sign position 1, negative value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'negative_sign': '-',
        'n_sign_posn': 1,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '-$1.00'


def test__currency__format_currency__output__sign_position_1_positive_following_cs():
    """Tests sign position 1, positive value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'positive_sign': '+',
        'p_sign_posn': 1
    }

    test_currency = currency.Currency(conventions)


    assert test_currency.format_currency('1.00') == '+1.00$'


def test__currency__format_currency__output__sign_position_1_negative_following_cs():
    """Tests sign position 1, negative value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'negative_sign': '-',
        'n_sign_posn': 1,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '-1.00$'


def test__currency__format_currency__output__sign_position_2_positive_preceding_cs():
    """Tests sign position 2, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'positive_sign': '+',
        'p_sign_posn': 2,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '$1.00+'


def test__currency__format_currency__output__sign_position_2_negative_preceding_cs():
    """Tests sign position 2, negative value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'negative_sign': '-',
        'n_sign_posn': 2,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '$1.00-'


def test__currency__format_currency__output__sign_position_2_positive_following_cs():
    """Tests sign position 2, positive value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'positive_sign': '+',
        'p_sign_posn': 2,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '1.00$+'


def test__currency__format_currency__output__sign_position_2_negative_following_cs():
    """Tests sign position 2, negative value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'negative_sign': '-',
        'n_sign_posn': 2,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '1.00$-'


def test__currency__format_currency__output__sign_position_3_positive_preceding_cs():
    """Tests sign position 3, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'positive_sign': '+',
        'p_sign_posn': 3,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '$+1.00'


def test__currency__format_currency__output__sign_position_3_negative_preceding_cs():
    """Tests sign position 3, negative value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'negative_sign': '-',
        'n_sign_posn': 3,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '$-1.00'


def test__currency__format_currency__output__sign_position_3_positive_following_cs():
    """Tests sign position 3, positive value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'positive_sign': '+',
        'p_sign_posn': 3,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '+1.00$'


def test__currency__format_currency__output__sign_position_3_negative_following_cs():
    """Tests sign position 3, negative value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'negative_sign': '-',
        'n_sign_posn': 3,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '-1.00$'


def test__currency__format_currency__output__sign_position_4_positive_preceding_cs():
    """Tests sign position 4, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'positive_sign': '+',
        'p_sign_posn': 4,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '$1.00+'


def test__currency__format_currency__output__sign_position_4_negative_preceding_cs():
    """Tests sign position 4, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'negative_sign': '-',
        'n_sign_posn': 4,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '$1.00-'


def test__currency__format_currency__output__sign_position_4_positive_following_cs():
    """Tests sign position 4, positive value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'positive_sign': '+',
        'p_sign_posn': 4,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '1.00+$'


def test__currency__format_currency__output__sign_position_4_negative_following_cs():
    """Tests sign position 4, negative value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'negative_sign': '-',
        'n_sign_posn': 4,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '1.00-$'


def test__currency__format_currency__output__sign_position_other_positive_preceding_cs():
    """Tests 'other' sign position, positive value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'positive_sign': '+',
        'p_sign_posn': None,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '+$1.00'


def test__currency__format_currency__output__sign_position_other_negative_preceding_cs():
    """Tests 'other' sign position, negative value, and preceding symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'negative_sign': '-',
        'n_sign_posn': None,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '-$1.00'


def test__currency__format_currency__output__sign_position_other_positive_following_cs():
    """Tests 'other' sign position, positive value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'p_cs_precedes': False,
        'positive_sign': '+',
        'p_sign_posn': None,
        }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('1.00') == '+1.00$'


def test__currency__format_currency__output__sign_position_other_negative_following_cs():
    """Tests 'other' sign position, negative value, and following symbol."""
    # Setup custom conventions for testing
    conventions = {
        'currency_symbol': '$',
        'n_cs_precedes': False,
        'negative_sign': '-',
        'n_sign_posn': None,
    }

    test_currency = currency.Currency(conventions)

    assert test_currency.format_currency('-1.00') == '-1.00$'
