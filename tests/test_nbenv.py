#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nbenv` package."""

import os
import subprocess
import pytest

from nbenv import nbenv
from nbenv import cli

TEST_ENV_INPUT_NAME = "nbenv_test_input_env"

@pytest.fixture(scope="module")
def setup_conda_environment():
    conda_package_list = os.path.join(os.path.dirname(__file__),
                                      "test_conda_list.txt")
    subprocess.run(["conda", "create", "--yes", "--name", TEST_ENV_INPUT_NAME,
                    "--file", conda_package_list], check=True)

def test_fixture(setup_conda_environment):
    """Check that the conda environment was created successfully"""
    test_conda_env_package_list = \
        subprocess.check_output(["conda", "list", "--export", "--name", TEST_ENV_INPUT_NAME])
    #TODO compare outputs


def test_command_line_interface():
    """Test the CLI."""
