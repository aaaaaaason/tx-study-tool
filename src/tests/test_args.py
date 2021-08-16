"""Test command line functions."""
import txtool
import pytest


@pytest.mark.small
def test_parse_args():
    # When I start this program.
    env = 'env_path'
    case = 'case_path'
    ns = txtool.parse_args(['--env', env, case])

    # Then I should get the same values from input.
    assert ns.env == env,\
        f'Expect env to be {env}, got {ns.env}.'

    assert ns.case == case,\
        f'Expect case to be {case}, got {ns.case}.'


@pytest.mark.small
def test_parse_args_default_env_path():
    # When I start this program.
    case = 'case_path'
    ns = txtool.parse_args([case])

    # Then I should get default env path.
    assert ns.env == '.env',\
        f'Expect env to be .env, got {ns.env}.'


@pytest.mark.small
def test_parse_args_no_case():
    # Then I should get no case argument error.
    with pytest.raises(SystemExit):
        # When I start this program.
        txtool.parse_args([])
