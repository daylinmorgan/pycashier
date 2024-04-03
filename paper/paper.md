---
title: 'Pycashier: cash in on DNA barcode tags'
tags:
  - python
  - sequencing
  - DNA barcoding
  - pipeline
authors:
  - name: Daylin Morgan
    orcid: 0000-0002-4218-2805
    affiliation: 1
  - name: Amy Brock
    orcid: 0000-0001-8255-9024
    corresponding: true
    affiliation: 1
affiliations:
 - name: The University of Texas at Austin, USA
   index: 1
date: 04 April 2024
bibliography: paper.bib
---

# Summary

`Pycashier` is a tool designed to extract DNA barcode tags from next generation sequencing data.
It was originally developed for use with the
ClonMapper Barcoding System [@alkhafaji2018;@gardner2024;@gardner2022].
`Pycashier` has been previously utilized to interrogate
tumor heterogeneity in barcoded cancer cell-line models [@gutierrez2021;@johnson2020],
however, it is generalizable to similar DNA barcoding systems with known flanking regions.


# Statement of need

DNA sequencing and DNA barcoding specifically, have become
more common as a modality for the characterization of clonal and lineage-specific subpopulations of cells.
As researchers leverage these technologies, they'll require tools easy to setup
and use to facilitate downstream biological analysis.
DNA barcode sequencing data is prone to noise from both preparation
and sequencing that requires identification and correction prior to statistical testing.
`Pycashier` fills this gap while also providing a simple-to-use interface.

# Implementation and Usage

`Pycashier` was intentionally designed to be simple-to-use for both computational and experimental biologists.
It accomplishes this by leveraging purpose-built software for an opinionated DNA barcode processing pipeline.
`Pycashier` has a command-line interface (CLI) implemented in `python`.
Users have the option of installing `pycashier` with `pip`, `conda/mamba` (from conda-forge),
or as a standalone `Docker` image which includes all necessary runtime dependencies for maximum reproducibility.
`Pycashier` maintains outputs and logs of all steps for simple debugging and reuse across a project.
The `pycashier` CLI has four subcommands to facilitate processing of DNA barcode sequencing data.
Users can specify parameters either through command-line flags or through a `toml` file.

`Pycashier` is primarily used for generating counts of individual barcode sequences
from targeted PCR (Polymerase Chain Reaction) amplifications of DNA-barcoded cells.
This is done with `pycashier extract`, which accepts a directory of
`fastq` files directly from Illumina sequencing and generates
a `tsv` of individual barcodes and counts for each input `fastq`.
First, filtering is performed with `fastp` [@chen2018] to remove low quality sequencing reads.
Next, flanking sequences are used to extract a region of interest with `cutadapt` [@martin2011].
Then, the list of identified sequences are corrected for errors introduced in either preparation
or sequencing using a message passing clustering powered by `starcode` [@zorita2015].
Finally, minimal count filtering is applied to remove any remaining noise from sequencing.

In addition to barcode extraction from targeted sequencing, `pycashier` facilitates
barcode extraction from single-cell RNA-sequencing (scRNA-seq).
Specifically, it's compatible with data generated with the 10X Genomics 3' based single cell gene expression kit.
In this case, the command `pycashier scrna` accepts `sam` files derived from processed 
`10X` data and generates a `tsv` with cell/UMI resolved barcode sequences,
which can then be mapped directly back to the transcriptome of individual cells.
To accomplish this, `pycashier` first extracts cell/UMI and
read sequences from `sam` files using `pysam` [@pysam2024].
Next, sequences are individually extracted from `fastq` files again,
using `cutadapt` with known flanking sequences.

`Pycashier` provides two additional convenience commands:
`merge`, to generate single read consensus sequences
from paired-end sequencing, and `reciept`,
to combine output `tsv` files from `pycashier extract`
along with calculating some basic metrics across samples.

Documentation and further usage instructions for `pycashier`
can be found at [docs.brocklab.com/pycashier](https://docs.brocklab.com/pycashier).

# Acknowledgments

We acknowledge Aziz Al'Khafaji for the development of the
ClonMapper Barcoding System, which drove the development of this tool.
The authors are grateful for support from NIH 1U01CA25354 (to A.B).

# References
