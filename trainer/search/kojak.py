"""
A module run Kojak
"""
import os
import re
import subprocess

# Setup ----------------------------------------------------------------------

# Functions ------------------------------------------------------------------
def configure(fasta, pre_tol, frag_bin, mods, enzymes, template):
    """
    Generate an appropriate Kojak parameter file based on a template.

    The template file should have the following keys which this function
    will replace:
    $database$ - The fasta database.
    $fragbin$ - The fragment bin width.
    $pretol$ - The precursor tolerance.

    Parameters
    ----------
    fasta : str
        The path to the appropriate FASTA file for the dataset.

    pre_tol : float
        The precursor ion tolerance in ppm.

    frag_bin : float
        The fragment bin width in m/z.

    mod : list
        Variable modifications to consider. These must be updated in the
        mods variable in config.py if a new one is used.

    enzymes : list
        The enzymes to consider. These must be updated in the enzymes
        variable of config.py.

    Returns
    -------
    str
        A new Kojak configuration file in a string.
    """
    mod_conf = "\n".join(config.mods[mod]["kojak"] for mod in mods)
    enz_conf = "\n".join(config.enzymes[enz]["kojak"] for enz in enzymes)

    with open(template) as base_file:
        conf = base_file.reas()

    conf = re.sub(r"\$database\$", fasta, conf)
    conf = re.sub(r"\$fragbin\$", str(frag_bin), conf)
    conf = re.sub(r"\$pretol\$", str(pre_tol), conf)
    conf = conf + "\n" + mod_conf + "\n" + enz_conf

    return conf


def run(mzml_files, conf_file, data_dir):
    """
    Run Kojak.

    Parameters
    ----------
    mzml_files : list
        A list of mzML files to search.

    conf_file : str
        The Kojak configuration file to use.

    data_dir : str
        Where to write the results
    """
