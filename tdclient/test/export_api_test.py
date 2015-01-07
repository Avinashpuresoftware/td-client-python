#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

try:
    from unittest import mock
except ImportError:
    import mock
import pytest

from tdclient import api
from tdclient.test.test_helper import *

def setup_function(function):
    unset_environ()

def test_export_success():
    td = api.API("APIKEY")
    # TODO: should be replaced by wire dump
    body = b"""
        {
            "job_id": "12345"
        }
    """
    td.post = mock.MagicMock(return_value=response(200, body))
    job = td.export_data("db", "table", "s3")
    td.post.assert_called_with("/v3/export/run/db/table", {"storage_type": "s3"})
    assert job == "12345"

def test_export_failure():
    td = api.API("APIKEY")
    td.post = mock.MagicMock(return_value=response(500, b"error"))
    with pytest.raises(api.APIError) as error:
        td.export_data("db", "table", "s3")
    assert error.value.args == ("500: Export failed: error",)
