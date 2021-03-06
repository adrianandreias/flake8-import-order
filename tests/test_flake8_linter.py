import ast
import re
import os

import pep8
import pytest

from flake8_import_order.flake8_linter import Linter

from tests.utils import extract_expected_errors


def load_test_cases():
    base_path = os.path.dirname(__file__)
    test_case_path = os.path.join(base_path, "test_cases")
    test_case_files = os.listdir(test_case_path)

    test_cases = []

    for fname in test_case_files:
        if not fname.endswith(".py"):
            continue

        fullpath = os.path.join(test_case_path, fname)
        data = open(fullpath).read()
        tree = ast.parse(data, fullpath)
        expected = extract_expected_errors(data)

        test_cases.append((tree, fullpath, expected))

    return test_cases


@pytest.mark.parametrize(
    "tree, filename, expected",
    load_test_cases()
)
def test_expected_error(tree, filename, expected):
    parser = pep8.get_parser('', '')
    Linter.add_options(parser)
    options, args = parser.parse_args(
        ['--import-order-style=google'] if 'google' in filename else [])
    Linter.parse_options(options)

    checker = Linter(tree, filename)
    errors = []
    for lineno, col_offset, msg, instance in checker.run():
        errors.append(msg.split()[0])
    assert errors == expected
