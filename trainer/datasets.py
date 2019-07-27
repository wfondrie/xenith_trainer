"""
Define the training, validation and tests sets for xenith models.
"""
import os
import logging
from typing import Tuple

import xenith

# Trainer modules
import download
import crux
import msconvert
import search.kojak as kojak


# Get environment variables ---------------------------------------------------
DATAPATH = os.getenv("DATAPATH", "./data")

# Classes ---------------------------------------------------------------------
class TrainerDatasets():
    """
    A class to hold information about datasets for xenith models.

    Attributes
    ----------
    training : list of XLDataset
        The training set used to train the models included with xenith.

    validation : list of XLDataset
        The validation set used to train the models included with
        xenith.

    test : list of XLDatset
        The test set used to evaluate how well the xenith models are
        performing.
    """
    def __init__(self):
        """Initialize a TrainerDatasets object"""
        self.training = []
        self.validation = []
        self.test = []

    def add_dataset(**kwargs) -> None:
        """Add a dataset to the TrainerDatasets object"""
        dataset = XLDataset(**kwargs)

        if dataset.split == "training":
            self.training.append(dataset)
        elif dataset.split == "validation":
            self.validation.append(dataset)
        elif dataset.split == "test":
            self.test.append(dataset)
        else:
            raise ValueError(f"Unknown value for 'split' in "
                             "{dataset.pxid}.")

    def search_all(self, split, engine="kojak", **kwargs) -> None:
        """Run a Kojak searches on all of the datasets."""
        pass


class XLDataset():
    """
    A class to hold information about individual datasets.

    Parameters
    ----------
    pxid : str
        The ProteomeXchange ID of the dataset.

    raw_files : list of str
        The raw mass spectrometry files(.raw, .wiff, etc.) to be
        included.

    mods : list of str
        List indicating the variable modifications, including the
        cross-linker. This must be defined in the MOD_SPEC variable at
        the beginning of this file. The run() function for 

    enzymes : list of str
        String indicating enzymes.

    fasta : str or list of str
        The provided protein database in fasta format, a list of proteins,
        or a uniprot taxonomy.

    fasta_type : str
        The type of input in fasta ("fasta", "proteins", "proteome")

    split : str
        Indicates whether this dataset is part of the training,
        validation, or test data split.

    Attributes
    ----------
    pxid : str
        The ProteomeXchange ID of the dataset.

    raw_files : list of str
        The raw mass spectrometry data files.

    mzml_files : list of str
        Path to the mzML files.

    fasta_file : str
        Path to the fasta file to search against.

    mods : str
        List indicating the variable modifications to consider,
        including the cross-linker.

    split : str
        Indicates whether this dataset is part of the training,
        validation, or test data split.

    path : str
        Path where all the data is saved.
    """
    def __init__(self,
                 pxid: str,
                 raw_files: Tuple[str],
                 fasta: Tuple[str],
                 fasta_type: str,
                 mods: Tuple[str] = ("BS3",),
                 enzymes: Tuple[str] = ("trypsin",),
                 split: str = "training") -> None:
        """Instantiate an XLDataset object"""
        self.pxid = pxid
        self.raw_files = raw_files
        self.mods = mods
        self.enzymes = enzymes
        self.split = split

        logging.info(pxid)
        self.path = os.path.join("DATAPATH", split, pxid)
        logging.info("Path = %s", path)

        # Download if it does not already exist.
        self.fasta_file = os.path.join(self.path, self.pxid + ".fasta")
        if not os.path.isfile(self.fasta_file):
            logging.info("FASTA file not detected.")
            self._download_fasta(fasta, fasta_type)

        # Check for mzML files.
        if isinstance(raw_files, str):
            self.raw_files = (raw_files,)

        self.mzml_files = [f.replace(".+?$", ".mzML.gz")
                           for f in self.raw_files]
        self.mzml_files = [os.path.join(self.path, f)
                           for f in self.mzml_files]

        if not self._mzml_exist():
            logging.info("mzML files not detected. Please download and "
                         "convert before proceeding.")
        else:
            logging.info("All FASTA and mzML files are present.")

    def _download_fasta(self, fasta, fasta_type):
        """
        Download a fasta in one of 3 ways:

        If fasta_type == "fasta", the fasta file is downloaded from the
        PRIDE repository for the dataset.

        If fasta_type == "proteins", download the sequences for the list
        of Uniprot identifiers provided.

        If fasta_type == "proteome", download the proteome from
        Uniprot's reference proteomes.

        In any case, once the fasta is assembled, crux is used to create
        a Target-Decoy database from the entries.
        """
        pass

    def search(self, engine: str = "kojak", **kwargs) -> Tuple[str]:
        """
        Search the dataset using the search engine specified by 'engine'.

        Parameters
        ----------
        engine : str
            The search engine to use. The available **kwargs will differ
            based on the search engine that is chosen.

        Returns
        -------
        Tuple[str]
            A tuple of length 2 containing the xenith and pin output
            locations respectively.
        """
        if not self._mzml_exist:
            raise RuntimeError("mzML files do not exist.")

        if engine == "kojak":
            search.kojak.run(self, **kwargs)




    def _mzml_exist(self):
        return all(os.path.isfile(f) for f in self.mzml_files)



