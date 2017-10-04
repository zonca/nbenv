# -*- coding: utf-8 -*-

"Notebook environment module, store and extract conda environment in .ipynb"
import os
import subprocess

import nbformat


# tools to extract metadata and create a conda environment


def extract_package_list(notebook_filename):
    """Extract package list stored in notebook metadata"""

    with open(notebook_filename, mode="r", encoding="utf-8") as file_handle:
        conda_package_list = nbformat.read(
            file_handle,
            as_version=nbformat.NO_CONVERT
        )["metadata"]["conda_package_list"]

    return conda_package_list


def write_package_list_file(package_list, package_list_filename):
    """Write a package list to file"""
    with open(package_list_filename, "w") as file_handle:
        file_handle.write(package_list)


def extract_and_write_package_list(notebook_filename, package_list_filename=None):
    """Dumps package list from notebook to STOUT or a file"""
    package_list = extract_package_list(notebook_filename)
    if package_list_filename:
        write_package_list_file(package_list, package_list_filename)
        print("Extracted list of packages to {}".format(package_list_filename))
    else:
        print(package_list)


def create_conda_environment(env_name,
                             package_list_filename,
                             conda_create_extra_args=None):
    """Create a conda env from packages exported with conda list --export"""
    command = ["conda", "create", "--yes",
               "--name", env_name,
               "--file", package_list_filename]
    if conda_create_extra_args:
        try:
            command += conda_create_extra_args
        except:
            print("conda_create_extra_args should be a list of arguments," +
                  " e.g. ['numpy=1.13','--verbose']")
            raise
    subprocess.run(command, check=True)


def install_ipykernel(env_name, kernel_display_name):
    """Install an IPython kernel for the conda environment"""
    subprocess.run((
        "python -m ipykernel install --user" +
        " --name {env_name} --display-name {kernel_display_name}"
        .format(
            env_name=env_name,
            kernel_display_name=kernel_display_name)).split(),
        check=True)


def create_conda_env_from_notebook(notebook_filename,
                                   env_name=None,
                                   kernel_display_name=None,
                                   conda_create_extra_args=None):
    """Create a new conda environment from metadata stored in a Notebook file


    Parameters
    ---------
    notebook_filename : path to .ipynb file
        Input notebook, it should have used the nbenv pre_save_hook to save
        metadata about the conda environment
    env_name : string
        Name of the conda environment to be created, by default it is nbenv_ +
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

    package_list_filename = "package_list_{}.txt".format(env_name)
    extract_and_write_package_list(notebook_filename, package_list_filename)

    create_conda_environment(env_name,
                             package_list_filename,
                             conda_create_extra_args)
    print("Created conda environment {}".format(env_name))

    install_ipykernel(env_name, kernel_display_name)
    print("Installed IPython Kernel with display name {}".format(
        kernel_display_name
        ))
