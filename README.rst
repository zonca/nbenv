=====
nbenv
=====


.. image:: https://img.shields.io/pypi/v/nbenv.svg
        :target: https://pypi.python.org/pypi/nbenv

.. image:: https://img.shields.io/travis/zonca/nbenv.svg
        :target: https://travis-ci.org/zonca/nbenv

Store conda environment package list inside Notebook documents

This package provides a hook for the Jupyter Notebook that saves metadata about the
conda environment (equivalent of `conda env export`) inside the Notebook `.ipynb` file
everytime that the Notebook is saved.
It also supports packages installed inside the conda environment with `pip`.

Once such Jupyter Notebook is shared, another user can inspect the environment where
it ran:

.. code-block:: bash

    $ nbenv --extract my_notebook.ipynb

    name: test_input_env
    channels:
    - defaults
    - conda-forge
    dependencies:
    - ca-certificates=2017.08.26=h1d4fec5_0
    - certifi=2017.7.27.1=py35h19f42a1_0
    - decorator=4.1.2=py35h3a268aa_0
    - ipykernel=4.6.1=py35h29d130c_0
    - ipython=6.1.0=py35h1b71439_1
    - ipython_genutils=0.2.0=py35hc9e07d0_0
    - jupyter_client=5.1.0=py35h2bff583_0
    - pip:
      - ipython-genutils==0.2.0
      - jupyter-client==5.1.0

And re-create the same environment (includes install of IPython Kernel):

.. code-block:: bash

    $ nbenv my_notebook.ipynb --name reconstructed_env
    $ source activate reconstructed_env
    $ jupyter notebook

The environment metadata will be preserved if the Notebook file is modified by a Jupyter Notebook session
with no ``nbenv`` installed.

Install
--------

Install the package with `pip install nbenv`

Install the Jupyter Notebook hook in your `.jupyter/jupyter_notebook_config.py`:

.. code-block:: python

    try:
        from nbenv import save_conda_environment
        c.FileContentsManager.pre_save_hook = save_conda_environment
    except ImportError:
        print("nbenv package not found: automatic saving of conda environment disabled")

Implementation details
----------------------

The `pre_save_hook` is automatically triggered by the Jupyter Notebook before saving the Notebook
to disk.
It identifies the conda environment being run checking the KernelSpec and then calls ``conda env export``
and saves the output in ``["content"]["metadata"]["conda_environment"]`` in the ``.ipynb`` JSON.

The ``nbenv`` command line tool can then extract that and use ``conda create`` to a new environment.

Credits
---------

Design of this package was conceived during discussion at the `Container Analysis Environments Workshop`_
held at NCSA in August 2017.

.. _`Container Analysis Environments Workshop`: https://nationaldataservice.atlassian.net/wiki/spaces/NDSC/pages/37284774/Container+Analysis+Environments+Workshop

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

