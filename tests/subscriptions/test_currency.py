"""Tests for the currency module."""
from decimal import Decimal

from subscriptions import currency


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
