# -*- coding: utf-8 -*-

"""Top-level package for nbenv."""

__author__ = """Andrea Zonca"""
__email__ = 'code@andreazonca.com'
__version__ = '0.1.4'

from .nbenv import create_conda_env_from_notebook
from .hooks import save_conda_environment
