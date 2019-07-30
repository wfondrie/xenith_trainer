"""
Download fasta files, or create a new fasta from a list of proteins.

There may be some issues, due to poorly name files in PRIDE and other
hiccups, so some PXIDs need special treatment.
"""
import os
import io
import gzip
import urllib.request as request
from contextlib import closing

import ppx
import bioservices

# Setup -----------------------------------------------------------------------
# Some datasets will require special treatment:
SPECIAL = ["PXD004074", "PXD010222"]

# Functions -------------------------------------------------------------------
def download_from_pride(pxdataset, fasta, data_dir):
    """
    Download available FASTA files from the PRIDE repository.

    Parameters
    ----------
    pxdataset : ppx.PXDataset
        A ppx.PXDataset() where the FASTA is located.

    fasta : str
        The specific FASTA file to download.

    data_dir : str
        The directory where the FASTA will be downloaded.
    """
    if pxdataset.pxid in SPECIAL:
        download_special(pxdataset, data_dir)
    else:
        pxdataset.pxget(fasta, dest_dir=data_dir)
        os.path.join(data_dir, fasta)


def download_special(pxdataset, data_dir):
    """Handle odd protein databases"""
    # PXD004074 (Tsr1) --------------------------------------------------------
    if pxdataset.pxid == "PXD004074":
        tsr1_filename = "Rappsilber_Cook_CLMS_Tsr1_fasta.zip"
        tsr1_zip = os.path.join(data_dir, tsr1_filename)
        pxdataset.pxget(tsr1_filename, data_dir)

        with zipfile.ZipFile(tsr1_zip, "r") as fname:
            fname.extractall(data_dir)

    # PXD010222 (PPARg_LBD) ---------------------------------------------------
    if pxdataset.pxid == "PXD010222":
        ppar_seq = [
            ">wef|PV4545|PPARg-LBD_human GST-tagged PPARgamma LBD",
            "MAPILGYWKIKGLVQPTRLLLEYLEEKYEEHLYERDEGDKWRNKKFELGLEFPNLPYYIDGD",
            "VKLTQSMAIIRYIADKHNMLGGCPKERAEISMLEGAVDIRYGVSRIAYSKDFETLKVDFLSK",
            "LPEMLKMFEDRLCHKTYLNGDHVTHPDFMLYDALDVVLYMDPMCLDAFPKLVCFKKRIEAIP",
            "QIDKYLKSSKYIALWPLQGWQATFGGGDHPPKSDLVPRHNQTSLYKKAGTMQLNPESADLRA",
            "LAKHLYDSYIKSFPLTKAKARAILTGKTTDKSPFVIYDMNSLMMGEDKIKFKHITPLQEQSK",
            "EVAIRIFQGCQFRSVEAVQEITEYAKSIPGFVNLDLNDQVTLLKYGVHEIIYTMLASLMNKD",
            "GVLISEGQGFMTREFLKSLRKPFGDFMEPKFEFAVKFNALELDDSDLAIFIAVIILSGDRPG",
            "LLNVKPIEDIQDNLLQALELQLKLNHPESSQLFAKLLQKMTDLRQIVTEHVQLLQVIKKTET",
            "DMSLHPLLQEIYKDL"
        ]

        ppar_path = os.path.join(data_dir, "pparg.fasta")
        with open(ppar_path, "w") as fasta:
            fasta.writelines([l + "\n" for l in ppar_seq])

def download_proteins(proteins, data_dir, fileroot="uniprot"):
    """
    Given a list of proteins, download their sequences to a FASTA file.

    Parameters
    ----------
    proteins : Tuple[str]
        Uniprot accessions to retrieve

    data_dir : str
        Where to download the FASTA file.

    fileroot : str
        How should the file be named?

    Returns
    -------
    str
        The FASTA file created.
    """
    uniprot = bioservices.UniProt()
    outfile = os.path.join(data_dir, fileroot + ".fasta")
    with open(outfile, "w") as fasta_out:
        lines = uniprot.retrieve(proteins, frmt="fasta")
        lines = "".join(lines)
        fasta_out.write(lines)

    return outfile


def download_proteome(proteome_id, data_dir, domain="Eukaryota"):
    """
    Download the UniProt reference proteome for the given taxonomy.

    Parameters
    ----------
    proteome_id : str
        The UniProt proteome identifier for the species of interest.
        For example, human: "UP000005640_9606"

    domain : str
        Domain of the organism. Must be one of "Archaea", "Bacteria",
        "Eukaryota", or "Viruses".

    data_dir: str
        Where should the file be saved.
    """
    base = ("ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/"
            "knowledgebase/reference_proteomes")

    url = [base, domain, proteome_id + ".fasta.gz"]
    outfile = os.path.join(data_dir, proteome_id + ".fasta")

    with closing(request.urlopen(url)) as remote_handle:
        with open(remote_handle, "rb") as remote_file:
            mem_file = io.BytesIO(remote_file.read())

    with open(outfile, "w") as out, gzip.open(mem_file) as gz:
        outfile.write(gz.read())

    return outfile

