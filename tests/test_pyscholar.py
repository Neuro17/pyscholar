#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.query import Query

"""
test_pyscholar
----------------------------------

Tests for `pyscholar` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from pyscholar import pyscholar
from pyscholar import cli


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pyscholar.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_query_build():
    q = Query(authors=['page', 'brin'], words=['pagerank'],
              phrase='bringing order to the web')
    assert q.build() == 'https://scholar.google.it/scholar?as_oq=&lookup=0&as_sauthors=page+brin&hl=en&as_q=pagerank&as_eq=&as_vis=&as_epq=bringing+order+to+the+web'
