# -*- coding: utf-8 -*-

"""Console script for nbenv."""

import argparse
from .nbenv import extract_and_write_environment, create_conda_env_from_notebook

import sys


class PrintHelpOnErrorParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def main():
    """Console script for nbenv."""

    parser = PrintHelpOnErrorParser(
        description="Create a conda env from a package list stored in Notebook metadata"
    )
    parser.add_argument("notebook_filename",
        help="Input notebook saved with the nbenv pre save hook")
    parser.add_argument("--extract", action='store_true',
        help="Only dump the package list to stdout")
    parser.add_argument("other_conda_create_args", nargs=argparse.REMAINDER,
        help="Additional arguments for conda env create, like --name or --force")
    args = parser.parse_args()

    if args.extract:
        extract_and_write_environment(args.notebook_filename)
    else:
        create_conda_env_from_notebook(args.notebook_filename, extra_args=args.other_conda_create_args)


if __name__ == "__main__":
    main()
