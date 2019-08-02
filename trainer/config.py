"""
The configuration details for xenith_trainer.
"""
import os

# Program Binaries ------------------------------------------------------------
# Paths to the required program binaries should be specified in the following
# environment variables:
# KOJAK1 - The kojak 1.6.1 binary
# KOJAK2 - The kojak 2.0.0-dev binary
# CRUX - The crux binary
# RAWPARSER - The path to ThermoRawFileParser.exe

kojak = [{"version": "2.0.0-dev",
          "bin": "~/bin/kojak_2018-10-30/kojak",
          "template": "templates/kojak_2.0.0-dev.conf"},
         {"version": "1.6.1",
          "bin": "",
          "template": "templates/kojak_1.6.1.conf"}]

crux = "~/bin/crux"
ThermoRawFileParser = "~/bin/anaconda3/pkgs/thermorawfileparser-1.1.9-0/bin/ThermoRawFileParser.exe"

# Modifications and Enzymes ---------------------------------------------------
# This section defines valid modifications and enzymes. The dictionaries must
# include additions to the Kojak configuration file for the parameter.
# Enzymes are added as a list, with [cut-after, cut-before]. For example,
# Trypsin is ["KR", ""]. Suppression is not allowed.

mods = {
    "BS3": {
        "kojak": ("cross_link = nK nK 138.0680742 BS3\n"
                  "mono_link = nK 155.094629\n"
                  "mono_link = nK 156.078644\n")
    },
    "BS3-d4": {
        "kojak": ("cross_link = nK nK 142.093187 BS3-d4\n"
                  "mono_link = nK 159.119736\n"
                  "mono_link = nK 160.103751\n")
    },
    "BS3-d12": {
        "kojak": ("cross_link = nK nK 150.14339515 BS3-d12\n"
                  "mono_link = nK 167.16994995\n"
                  "mono_link = nK 168.15396495\n")
    }
}

enyzmes = {
    "Trypsin": ["KR", ""],
    "GluC": ["DE", ""],
    "Chymo": ["FWY", ""]
}

# The Datasets ----------------------------------------------------------------
# Datasets are specified as Python dictionaries. Below, 'train_set' defines the
# training set, 'val_set' defines the validation set, and 'test_set' defines
# the test set. Each should be added with as a key indicating its
# ProteoemeXchange Identifier. Additionally, each data has two required fields
# and several optional fields for proper search configuration:
# 'raw_files' - A list of raw files associated with the dataset. All raw files
#               for a dataset must share the same parameters (fasta, mods, ...)
# 'fasta' - A fasta file, list of protein accessions, or proteome to download.
# 'fasta_type' - if 'fasta' is not a fasta file, the valid options are
#                "proteins", or "proteome".
# 'mods' - Specify the variable modifications to consider. These include cross-
#          linking reagents. They must be in the 'mods' dictionary above. The
#          default is ["BS3"]
# 'enzymes' - Specify the enzymes used for digestion. They must be in the
#             'enzymes' dictionary above. The default is ["trypsin"].

# Some datasets were attempted, but failed to work in the pipeline:
# PXD009079 files caused Kojak to crash.
# PXD003736 files failed to convert with msconvert.

train_set = {
    "PXD003282": {
        "raw_files": ["Sheppard_Werner_RNAPORF145_07.raw"],
        "fasta": ["P95989", "P95989", "Q980Z8", "P58192", "Q97ZX7", "Q980R2",
                  "P96036", "Q980K0", "Q980R1", "Q97ZJ9", "Q980A3", "Q7LXK4"],
        "fasta_type": "proteins"
    },
    "PXD001835": {
        "raw_files": ["Rappsilber_Earnshaw_CLMS_SMC2-SMC4_holo-complex-Band-ii_1.raw"],
        "fasta": ["F1NDN4", "Q90988", "A0A1D5P4P8", "A0A1D5P3B2", "F1NS98",
                  "F1NWM5", "E1BRP2", "Q8AWB7", "Q8AWB8", "A0A1D5PM87"],
        "fasta_type": "proteins"
    },
    "PXD001675": {
        "raw_files": ["Chen_Rappsilber_QCLMS_xC3d0C3bd4_III.raw"],
        "fasta": ["P01014"],
    },
    "PXD004898": {
        "raw_files": ["dataset7_QEP2_DFA_chymot-tryp_BS3_1_040615.raw"],
        "fasta": ""
    },
    "PXD008868": {
        "raw_files": ["20170120_Fusion1_SA_MM_CSA-GFP_xlink_BS3_WCL_techRep1.raw"],
        "fasta": ""
    },
    "PXD008215": {
        "raw_files": ["Zou_Rappsilber_JW_MCAK_Unphosphorylated.raw"],
        "fasta": ""
    },
    "PXD007250": {
        "raw_files": ["B160815_05_Lumos_FM_IN_190_HSA_BS3_DDA_R_-DMSO_004.raw"],
        "fasta": ""
    },
    "PXD003678": {
        "raw_files": ["Zou_Rappsilber_JW_Dam1_Subcomplex_BS3_2015.raw"],
        "fasta": ""
    },
    "PXD006707": {
        "raw_files": ["20160201_Debelyy_8078-SCX5.raw"],
        "fasta": ""
    },
    "PXD005948": {
        "raw_files": ["JL082114_082814_SwiSnf5mM_30B.raw"],
        "fasta": ""
    },
    "PXD003486": {
        "raw_files": ["Chen_Rappsilber_QCLMS_xC3bd0iC3d4_II.raw"],
        "fasta": ""
    },
    "PXD010222": {
        "raw_files": ["3PPARG_LBD_Rosi.raw"],
        "fasta": ""
    },
    "PXD006626": {
        "raw_files": ["Cheatomium_ProtSEC_frac7-10_pepSEC11.raw"],
        "fasta": ""
    },
    "PXD004074": {
        "raw_files": ["Rappsilber_Cook_CLMS_Tsr1_WildType1.raw"],
        "fasta": ""
    }
}

val_set = {
    "PXD012723": {
        "raw_files": ["P2CH20181009_MU10.raw",
                      "P2CH20181009_MU8.raw",
                      "P2CH20181009_MU9.raw"],
        "fasta": ""
    },
    "PXD006246": {
        "raw_files": ["Rappsilber_CLMS_AUGMIN_1.raw",
                      "Rappsilber_CLMS_AUGMIN_2.raw",
                      "Rappsilber_CLMS_AUGMIN_3.raw"],
        "fasta": ""
    },
    "PXD002987": {
        "raw_files": ["xlink_PRPS1_rep1.raw",
                      "xlink_PRPS1_rep2.raw"],
        "fasta": ""
    }
}

test_set = {
    "PXD010481": {
        "raw_files": ["Rappsilber_CLMS_PolII_1.RAW",
                      "Rappsilber_CLMS_PolII_2.RAW",
                      "Rappsilber_CLMS_PolII_3.raw",
                      "Rappsilber_CLMS_PolII_4.RAW"],
        "fasta": ""
    }
}

