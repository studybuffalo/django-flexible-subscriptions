"""Tests for the conf module."""
from decimal import Decimal

from django.conf import settings
from django.test import override_settings

from subscriptions.conf import compile_settings, Currency, CURRENCY


@override_settings(
    DFS_ENABLE_ADMIN=1,
    DFS_CURRENCY_LOCALE=2,
    DFS_BASE_TEMPLATE='3'
)
def test_all_settings_populate_from_settings_properly():
    """Tests that Django settings all proper populate SETTINGS."""
    subscription_settings = compile_settings()

    assert len(subscription_settings) == 3
    assert subscription_settings['enable_admin'] == 1
    assert subscription_settings['currency_locale'] == '2'
    assert subscription_settings['base_template'] == '3'

@override_settings()
def test_settings_defaults():
    """Tests that SETTINGS adds all defaults properly."""
    # Clear any settings already provided
    del settings.DFS_ENABLE_ADMIN
    del settings.DFS_CURRENCY_LOCALE
    del settings.DFS_BASE_TEMPLATE

    subscription_settings = compile_settings()

    assert len(subscription_settings) == 3
    assert subscription_settings['enable_admin'] is False
    assert subscription_settings['currency_locale'] == 'en_us'
    assert subscription_settings['base_template'] == 'subscriptions/base.html'

def test_format_currency_en_us():
    """Tests that format currency works properly with the default."""
    currency_value = CURRENCY['en_us'].format_currency('1234567.987')

    assert currency_value == '$1,234,567.99'

def test_format_currency_rounding_string():
    """Tests that rounding works as expected with string values."""
    test_currency = Currency()

    assert test_currency.format_currency('0.506') == '0.51'
    assert test_currency.format_currency('0.505') == '0.51'
    assert test_currency.format_currency('0.5049') == '0.50'
    assert test_currency.format_currency('0.005') == '0.01'
    assert test_currency.format_currency('0.0049') == '0.00'
    assert test_currency.format_currency('-0.0049') == '0.00'
    assert test_currency.format_currency('-0.005') == '0.01'

def test_format_currency_rounding_decimal():
    """Tests that rounding works as expected with decimal values."""
    test_currency = Currency()

    assert test_currency.format_currency(Decimal('0.506')) == '0.51'
    assert test_currency.format_currency(Decimal('0.505')) == '0.51'
    assert test_currency.format_currency(Decimal('0.5049')) == '0.50'
    assert test_currency.format_currency(Decimal('0.005')) == '0.01'
    assert test_currency.format_currency(Decimal('0.0049')) == '0.00'
    assert test_currency.format_currency(Decimal('-0.0049')) == '0.00'
    assert test_currency.format_currency(Decimal('-0.005')) == '0.01'

def test_currency_format_grouping_by_1():
    """Tests that grouping works properly for groups of 1."""
    test_currency = Currency(mon_grouping=1, mon_thousands_sep=',')

    assert test_currency.format_currency('1.00') == '1.00'
    assert test_currency.format_currency('10.00') == '1,0.00'
    assert test_currency.format_currency('100.00') == '1,0,0.00'
    assert test_currency.format_currency('1000.00') == '1,0,0,0.00'

def test_currency_format_grouping_by_3():
    """Tests that grouping works properly for groups of 3."""
    test_currency = Currency(mon_grouping=3, mon_thousands_sep=',')

    assert test_currency.format_currency('1.00') == '1.00'
    assert test_currency.format_currency('10.00') == '10.00'
    assert test_currency.format_currency('100.00') == '100.00'
    assert test_currency.format_currency('1000.00') == '1,000.00'
    assert test_currency.format_currency('10000.00') == '10,000.00'
    assert test_currency.format_currency('100000.00') == '100,000.00'
    assert test_currency.format_currency('1000000.00') == '1,000,000.00'

def test_currency_format_grouping_separator():
    """Tests that the grouping separator is properly applied."""
    test_currency = Currency(mon_grouping=3, mon_thousands_sep='*')

    assert test_currency.format_currency('1000000.00') == '1*000*000.00'

def test_format_currency_symbol_precedes_positive():
    """Tests currency symbol is applied preceding positive value."""
    test_currency = Currency(currency_symbol='$', p_cs_precedes=True)

    assert test_currency.format_currency('1.00') == '$1.00'

def test_format_currency_symbol_precedes_negative():
    """Tests currency symbol is applied preceding negative value."""
    test_currency = Currency(currency_symbol='$', n_cs_precedes=True)

    assert test_currency.format_currency('-1.00') == '$1.00'

def test_format_currency_symbol_follows_positive():
    """Tests currency symbol is applied following positive value."""
    test_currency = Currency(currency_symbol='$', p_cs_precedes=False)

    assert test_currency.format_currency('1.00') == '1.00$'

def test_format_currency_symbol_follows_negative():
    """Tests currency symbol is applied following negative value."""
    test_currency = Currency(currency_symbol='$', n_cs_precedes=False)

    assert test_currency.format_currency('-1.00') == '1.00$'

def test_format_currency_symbol_precedes_with_space_positive():
    """Tests currency symbol is applied preceding positive value with space."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=True, p_sep_by_space=True
    )

    assert test_currency.format_currency('1.00') == '$ 1.00'

def test_format_currency_symbol_precedes_with_space_negative():
    """Tests currency symbol is applied preceding negative value with space."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=True, n_sep_by_space=True
    )

    assert test_currency.format_currency('-1.00') == '$ 1.00'

def test_format_currency_symbol_follows_with_space_positive():
    """Tests currency symbol is applied following positive value with space."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False, p_sep_by_space=True
    )

    assert test_currency.format_currency('1.00') == '1.00 $'

def test_format_currency_symbol_follows_with_space_negative():
    """Tests currency symbol is applied following negative value with space."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False, n_sep_by_space=True
    )

    assert test_currency.format_currency('-1.00') == '1.00 $'

def test_format_currency_symbol_international():
    """Tests that international currency symbol works properly."""
    test_currency = Currency(int_curr_symbol='USD')

    currency_string = test_currency.format_currency('1.00', international=True)

    assert currency_string == 'USD1.00'

def test_format_currency_sign_position_0_positive_preceding_cs():
    """Tests sign position 0, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', positive_sign='+', p_sign_posn=0
    )

    assert test_currency.format_currency('1.00') == '($1.00)'

def test_format_currency_sign_position_0_negative_preceding_cs():
    """Tests sign position 0, negative value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', negative_sign='-', n_sign_posn=0
    )

    assert test_currency.format_currency('-1.00') == '($1.00)'

def test_format_currency_sign_position_0_positive_following_cs():
    """Tests sign position 0, positive value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False,
        positive_sign='+', p_sign_posn=0
    )

    assert test_currency.format_currency('1.00') == '(1.00$)'

def test_format_currency_sign_position_0_negative_following_cs():
    """Tests sign position 0, negative value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False,
        negative_sign='-', n_sign_posn=0
    )

    assert test_currency.format_currency('-1.00') == '(1.00$)'

def test_format_currency_sign_position_1_positive_preceding_cs():
    """Tests sign position 1, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', positive_sign='+', p_sign_posn=1
    )

    assert test_currency.format_currency('1.00') == '+$1.00'

def test_format_currency_sign_position_1_negative_preceding_cs():
    """Tests sign position 1, negative value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', negative_sign='-', n_sign_posn=1
    )

    assert test_currency.format_currency('-1.00') == '-$1.00'

def test_format_currency_sign_position_1_positive_following_cs():
    """Tests sign position 1, positive value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False,
        positive_sign='+', p_sign_posn=1
    )

    assert test_currency.format_currency('1.00') == '+1.00$'

def test_format_currency_sign_position_1_negative_following_cs():
    """Tests sign position 1, negative value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False,
        negative_sign='-', n_sign_posn=1
    )

    assert test_currency.format_currency('-1.00') == '-1.00$'

def test_format_currency_sign_position_2_positive_preceding_cs():
    """Tests sign position 2, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', positive_sign='+', p_sign_posn=2
    )

    assert test_currency.format_currency('1.00') == '$1.00+'

def test_format_currency_sign_position_2_negative_preceding_cs():
    """Tests sign position 2, negative value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', negative_sign='-', n_sign_posn=2
    )

    assert test_currency.format_currency('-1.00') == '$1.00-'

def test_format_currency_sign_position_2_positive_following_cs():
    """Tests sign position 2, positive value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False,
        positive_sign='+', p_sign_posn=2
    )

    assert test_currency.format_currency('1.00') == '1.00$+'

def test_format_currency_sign_position_2_negative_following_cs():
    """Tests sign position 2, negative value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False,
        negative_sign='-', n_sign_posn=2
    )

    assert test_currency.format_currency('-1.00') == '1.00$-'

def test_format_currency_sign_position_3_positive_preceding_cs():
    """Tests sign position 3, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', positive_sign='+', p_sign_posn=3
    )

    assert test_currency.format_currency('1.00') == '$+1.00'

def test_format_currency_sign_position_3_negative_preceding_cs():
    """Tests sign position 3, negative value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', negative_sign='-', n_sign_posn=3
    )

    assert test_currency.format_currency('-1.00') == '$-1.00'

def test_format_currency_sign_position_3_positive_following_cs():
    """Tests sign position 3, positive value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False,
        positive_sign='+', p_sign_posn=3
    )

    assert test_currency.format_currency('1.00') == '+1.00$'

def test_format_currency_sign_position_3_negative_following_cs():
    """Tests sign position 3, negative value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False,
        negative_sign='-', n_sign_posn=3
    )

    assert test_currency.format_currency('-1.00') == '-1.00$'

def test_format_currency_sign_position_4_positive_preceding_cs():
    """Tests sign position 4, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', positive_sign='+', p_sign_posn=4
    )

    assert test_currency.format_currency('1.00') == '$1.00+'

def test_format_currency_sign_position_4_negative_preceding_cs():
    """Tests sign position 4, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', negative_sign='-', n_sign_posn=4
    )

    assert test_currency.format_currency('-1.00') == '$1.00-'

def test_format_currency_sign_position_4_positive_following_cs():
    """Tests sign position 4, positive value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False,
        positive_sign='+', p_sign_posn=4
    )

    assert test_currency.format_currency('1.00') == '1.00+$'

def test_format_currency_sign_position_4_negative_following_cs():
    """Tests sign position 4, negative value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False,
        negative_sign='-', n_sign_posn=4
    )

    assert test_currency.format_currency('-1.00') == '1.00-$'

def test_format_currency_sign_position_other_positive_preceding_cs():
    """Tests 'other' sign position, positive value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', positive_sign='+', p_sign_posn=None
    )

    assert test_currency.format_currency('1.00') == '+$1.00'

def test_format_currency_sign_position_other_negative_preceding_cs():
    """Tests 'other' sign position, negative value, and preceding symbol."""
    test_currency = Currency(
        currency_symbol='$', negative_sign='-', n_sign_posn=None
    )

    assert test_currency.format_currency('-1.00') == '-$1.00'

def test_format_currency_sign_position_other_positive_following_cs():
    """Tests 'other' sign position, positive value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', p_cs_precedes=False,
        positive_sign='+', p_sign_posn=None
    )

    assert test_currency.format_currency('1.00') == '+1.00$'

def test_format_currency_sign_position_other_negative_following_cs():
    """Tests 'other' sign position, negative value, and following symbol."""
    test_currency = Currency(
        currency_symbol='$', n_cs_precedes=False,
        negative_sign='-', n_sign_posn=None
    )

    assert test_currency.format_currency('-1.00') == '-1.00$'
