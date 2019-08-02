"""
Run crux commands.
"""
import os
import shutil
import tempfile
import subprocess

# Setup -----------------------------------------------------------------------

# Functions -------------------------------------------------------------------
def make_decoys(fasta, out_file, enzyme, seed=1):
    """
    Create a shuffled target-decoy database from a target fasta.

    Parameters
    ----------
    fasta : str
        Path to a FASTA file.

    out_file : str
        The path to save the new FASTA file to.

    seed : int
        The random seed
    """
    enz = f"[{enzyme[0]}]|[{enzyme[1]}]"
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["crux", "generate-peptides", "--output-dir", tmpdir,
               "--custom-enzyme", enz, "--seed", seed, fasta]

        subprocess.run(cmd)
        res = os.path.join(tmpdir, "generate-peptides, proteins.decoy.txt")

        with open(out_file, "wb") as fout:
            with open(fasta, "rb") as targets:
                shutil.copyfileobj(targets, fout)
            with open(res, "rb") as decoys:
                shutil.copyfileobj(decoys, fout)


def param_medic(mzml_files, pxid, data_dir):
    """
    Run crux param-medic on a set of raw files.

    Parameters
    ----------
    mzml_files : Tuple[str]
        The mzML files to run param-medic on.

    pxid : str
        The ProteomeXchange ID.

    data_dir: str
        Where the results should be saved.
    """
    charges = (0, 2, 3, 4, 5, 6, 7, 8, 9)
    charges = ",".join(str(c) for c in charges)

    out_dir = os.path.join(data_dir, "pm-out")
    cmd = ["crux", "param-medic",
           "--pm-chargets", charges,
           "--fileroot", pxid,
           "--output-dir", out_dir,
           "--pm-top-n-frag-peaks", "60",
           "--pm-min-peak-pairs", "140"]

    subprocess.run(cmd + mzml_files)
