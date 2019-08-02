"""
A module run Kojak
"""
import subprocess

import xenith

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


def run(mzml_files, conf_file, out_file, kojak_bin):
    """
    Run Kojak then convert results to xenith format.

    Parameters
    ----------
    mzml_files : list
        A list of mzML files to search.

    conf_file : str
        The Kojak configuration file to use.

    out_file : str
        Where to write the xenith result.

    kojak_bin : str
        The Kojak binary to use. The version should match the conf file
        used.

    Returns
    -------
    Tuple[str, str]
        A Tuple containing the path to the xenith and pin files.
    """
    file_base = [f.replace(".mzML.gz", "") for f in mzml_files]
    cmd = [kojak_bin, conf_file, mzml_files]
    subprocess.run(cmd)

    for base in file_base:
        intra = base + ".perc.intra.txt"
        inter = base + ".perc.inter.txt"
        kojak = base + ".kojak.txt"
        version = _get_version(kojak)
        out_file = base + f"_kojak-{version}.xenith.txt"
        out_pin = base + f"_kojak-{version}.pin"

        xenith.convert.kojak(kojak, inter, intra, out_file,
                             version=version)
        xenith.convert.kojak(kojak, inter, intra, out_pin,
                             version=version, to_pin=True)

        return (out_file, out_pin)


def _get_version(kojak_txt):
    """
    Get the Kojak version from the first line of the result file.
    """
    with open(kojak_txt) as kojak_file:
        version = kojak_file.readline()

    return version.replace("Kojak version ", "")
