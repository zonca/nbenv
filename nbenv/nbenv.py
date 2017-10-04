# -*- coding: utf-8 -*-

"Notebook environment module, store and extract conda environment in .ipynb"
import os
import subprocess

import nbformat


# tools to extract metadata and create a conda environment


def extract_environment(notebook_filename):
    """Extract package list stored in notebook metadata"""

    with open(notebook_filename, mode="r", encoding="utf-8") as file_handle:
        conda_environment = nbformat.read(
            file_handle,
            as_version=nbformat.NO_CONVERT
        )["metadata"]["conda_environment"]

    return conda_environment


def write_environment_file(environment, environment_filename):
    """Write a package list to file"""
    with open(environment_filename, "w") as file_handle:
        file_handle.write(environment)


def extract_and_write_environment(notebook_filename, environment_filename=None):
    """Dumps package list from notebook to STOUT or a file"""
    environment = extract_environment(notebook_filename)
    if environment_filename:
        write_environment_file(environment, environment_filename)
        print("Extracted list of packages to {}".format(environment_filename))
    else:
        print(environment)


def create_conda_environment(env_name,
                             environment_filename,
                             extra_args=None):
    """Create a conda env from packages exported with conda env export"""
    command = ["conda", "env", "create",
               "--name", env_name,
               "--file", environment_filename]
    if extra_args:
        try:
            command += extra_args
        except:
            print("extra_args should be a list of arguments," +
                  " e.g. ['numpy=1.13','--verbose']")
            raise
    subprocess.run(command, check=True)


def install_ipykernel(env_name, kernel_display_name):
    """Install an IPython kernel for the conda environment"""
    subprocess.run((
        "bash -c \"source activate {env_name};" +
        "python -m ipykernel install --user" +
        " --name {env_name}" +
        " --display-name '{kernel_display_name}'\""
        ).format(env_name=env_name, kernel_display_name=kernel_display_name),
        check=True, shell=True)


def create_conda_env_from_notebook(notebook_filename,
                                   env_name=None,
                                   kernel_display_name=None,
                                   extra_args=None):
    """Create a new conda environment from metadata stored in a Notebook file


    Parameters
    ---------
    notebook_filename : path to .ipynb file
        Input notebook, it should have used the nbenv pre_save_hook to save
        metadata about the conda environment
    env_name : string
        Name of the conda environment to be created, default is nbenv_ +
        the notebook filename without extension and with spaces replaced by _
    kernel_display_name : string
        Display name of the new IPython kernel to be installed
    """

    # process input
    notebook_basename = os.path.splitext(
        os.path.basename(notebook_filename.replace(" ", "_"))
        )[0]
    if not env_name:
        env_name = "nbenv_" + notebook_basename
    if not kernel_display_name:
        kernel_display_name = env_name.replace("_", " ")

    environment_filename = "environment_{}.yml".format(env_name)
    extract_and_write_environment(notebook_filename, environment_filename)

    create_conda_environment(env_name,
                             environment_filename,
                             extra_args)
    print("Created conda environment {}".format(env_name))

    install_ipykernel(env_name, kernel_display_name)
    print("Installed IPython Kernel with display name {}".format(
        kernel_display_name
        ))
