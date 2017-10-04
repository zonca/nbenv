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
                                      "env.yml")
    subprocess.run(["conda", "env", "create", "--force", "--name", TEST_ENV_INPUT_NAME,
                    "--file", conda_package_list], check=True)


def test_fixture(setup_conda_environment):
    """Check that the conda environment was created successfully"""
    subprocess.run(
        "conda list --export --name {env} > temp_conda_list.txt".format(env=TEST_ENV_INPUT_NAME),
        shell=True, check=True)
    subprocess.run(["diff", "-I", "^#", "temp_conda_list.txt",
        os.path.join(os.path.dirname(__file__), "test_conda_list.txt")], check=True)

def test_command_line_interface():
    """Test the CLI."""
