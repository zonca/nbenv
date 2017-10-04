import subprocess

import jupyter_client

# pre_save_hook
def save_conda_environment(model, **kwargs):
    """Save conda environment packages in notebook metadata

    It saves the output of `conda env export` in the notebook .ipynb
    JSON file inside content/metadata/environment
    It should be activated as `pre_save_hook` in `jupyter_notebook_config.py`:

        from nbenv import save_conda_environment
        c.FileContentsManager.pre_save_hook = save_conda_environment
    """
    # only run on notebooks
    if model["type"] != "notebook":
        return

    try:
        kernel_spec_name = model["content"]["metadata"]["kernelspec"]["name"]
    except KeyError:
        # probably .ipynb not yet created
        return

    print("Kernel spec", kernel_spec_name)
    kernel_spec = jupyter_client.kernelspec.get_kernel_spec(kernel_spec_name)

    # FIXME better way of finding prefix, possibly for other languages
    prefix = kernel_spec.argv[0].split("/bin/")[0]
    print(prefix)

    env = subprocess.run(
        ["conda", "env", "export", "--prefix", prefix],
        stdout=subprocess.PIPE).stdout
    print(env)
    model["content"]["metadata"]["conda_environment"] = env
