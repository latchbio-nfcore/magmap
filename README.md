<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/nf-core-magmap_logo_dark.png">
    <img alt="nf-core/magmap" src="docs/images/nf-core-magmap_logo_light.png">
  </picture>
</h1>

[![GitHub Actions CI Status](https://github.com/nf-core/magmap/actions/workflows/ci.yml/badge.svg)](https://github.com/nf-core/magmap/actions/workflows/ci.yml)
[![GitHub Actions Linting Status](https://github.com/nf-core/magmap/actions/workflows/linting.yml/badge.svg)](https://github.com/nf-core/magmap/actions/workflows/linting.yml)[![AWS CI](https://img.shields.io/badge/CI%20tests-full%20size-FF9900?labelColor=000000&logo=Amazon%20AWS)](https://nf-co.re/magmap/results)[![Cite with Zenodo](http://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-1073c8?labelColor=000000)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![nf-test](https://img.shields.io/badge/unit_tests-nf--test-337ab7.svg)](https://www.nf-test.com)

[![Nextflow](https://img.shields.io/badge/nextflow%20DSL2-%E2%89%A523.04.0-23aa62.svg)](https://www.nextflow.io/)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)
[![run with singularity](https://img.shields.io/badge/run%20with-singularity-1d355c.svg?labelColor=000000)](https://sylabs.io/docs/)
[![Launch on Seqera Platform](https://img.shields.io/badge/Launch%20%F0%9F%9A%80-Seqera%20Platform-%234256e7)](https://cloud.seqera.io/launch?pipeline=https://github.com/nf-core/magmap)

[![Get help on Slack](http://img.shields.io/badge/slack-nf--core%20%23magmap-4A154B?labelColor=000000&logo=slack)](https://nfcore.slack.com/channels/magmap)[![Follow on Twitter](http://img.shields.io/badge/twitter-%40nf__core-1DA1F2?labelColor=000000&logo=twitter)](https://twitter.com/nf_core)[![Follow on Mastodon](https://img.shields.io/badge/mastodon-nf__core-6364ff?labelColor=FFFFFF&logo=mastodon)](https://mstdn.science/@nf_core)[![Watch on YouTube](http://img.shields.io/badge/youtube-nf--core-FF0000?labelColor=000000&logo=youtube)](https://www.youtube.com/c/nf-core)

## Introduction

**nf-core/magmap** is a bioinformatics best-practice analysis pipeline for mapping reads to a (large) collections of genomes.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It uses Docker/Singularity containers making installation trivial and results highly reproducible. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies. Where possible, these processes have been submitted to and installed from [nf-core/modules](https://github.com/nf-core/modules) in order to make them available to all nf-core pipelines, and to everyone within the Nextflow community!

<!-- TODO nf-core: Add full-sized test dataset and amend the paragraph below if applicable -->

On release, automated continuous integration tests run the pipeline on a full-sized dataset on the AWS cloud infrastructure. This ensures that the pipeline runs on AWS, has sensible resource allocation defaults set to run on real-world datasets, and permits the persistent storage of results to benchmark between pipeline releases and other analysis sources.The results obtained from the full-sized test can be viewed on the [nf-core website](https://nf-co.re/magmap/results).

## Pipeline summary

1. Read QC ([`FastQC`](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/))
2. Present QC for raw reads ([`MultiQC`](http://multiqc.info/))
3. Quality trimming and adapters removal for raw reads ([`Trimm Galore!`](https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/))
4. Filter reads with [`BBduk`](https://sourceforge.net/projects/bbmap/)
5. Select reference genomes based on k-mer signatures in reads with [`SOURMASH`](https://sourmash.readthedocs.io/en/latest/) (Can be skipped.)
6. Quantification of genes identified in selected reference genomes:
   1. Generate index of selected reference genomes ([`BBmap index`](https://sourceforge.net/projects/bbmap/))
   2. Map clean reads to the reference genomes for quantification ([`BBmap`](https://sourceforge.net/projects/bbmap/))
   3. Get raw counts per each gene present in the genomes ([`Featurecounts`](http://subread.sourceforge.net)) -> TSV table with collected featurecounts output
7. Summarise genome statistics and taxonomy (Dependent on CheckM/CheckM2 and GTDB-Tk data.)
8. Summarise output.

## Usage

> [!NOTE]
> If you are new to Nextflow and nf-core, please refer to [this page](https://nf-co.re/docs/usage/installation) on how to set-up Nextflow. Make sure to [test your setup](https://nf-co.re/docs/usage/introduction#how-to-run-a-pipeline) with `-profile test` before running the workflow on actual data.

First, prepare a samplesheet with your input data that looks as follows:

`samplesheet.csv`:

```csv
sample,fastq_1,fastq_2
CONTROL_REP1,AEG588A1_S1_L002_R1_001.fastq.gz,AEG588A1_S1_L002_R2_001.fastq.gz
```

Each row represents a fastq file (single-end) or a pair of fastq files (paired end).

Then decide if you want to use a set of genomes specified by you, a Sourmash index file pointing to genomes available at NCBI or a combination.
To specify your own genomes, create a file looking as follows:

`genomes.csv`:

```csv
accno,genome_fna,genome_gff
e_coli,contigs/e_coli.fna.gz,gffs/e_coli.gff.gz
GCA_002688505.1,https://github.com/nf-core/test-datasets/raw/magmap/testdata/GCA_002688505.1_ASM268850v1_genomic.fna.gz,
```

Each row represents one genome. _Note_ that the `genome_fna` (contigs) field is required, but the `genome_gff` is not.
If the latter is missing, the genome will be annotated with Prokka.

Now, you can run the pipeline using:

```bash
nextflow run nf-core/magmap --input samplesheet.csv --genomeinfo genomes.csv --outdir <OUTDIR> -profile <docker/singularity/podman/shifter/charliecloud/conda/institute>
```

:::warning
Please provide pipeline parameters via the CLI or Nextflow `-params-file` option. Custom config files including those
provided by the `-c` Nextflow option can be used to provide any configuration _**except for parameters**_;
see [docs](https://nf-co.re/usage/configuration#custom-configuration-files).
:::

For more details and further functionality, please refer to the [usage documentation](https://nf-co.re/magmap/usage) and the [parameter documentation](https://nf-co.re/magmap/parameters).

## Pipeline output

To see the results of an example test run with a full size dataset refer to the [results](https://nf-co.re/magmap/results) tab on the nf-core website pipeline page.
For more details about the output files and reports, please refer to the
[output documentation](https://nf-co.re/magmap/output).

## Credits

nf-core/magmap was originally written by Danilo Di Leo [@danilodileo](https://github.com/danilodileo), Emelie Nilsson [@emnillson](https://github.com/emnilsson) and Daniel Lundin [@erikrikardaniel](https://github.com/erikrikarddaniel).

## Contributions and Support

If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).

For further information or help, don't hesitate to get in touch on the [Slack `#magmap` channel](https://nfcore.slack.com/channels/magmap) (you can join with [this invite](https://nf-co.re/join/slack)).

## Citations

<!-- TODO nf-core: Add citation for pipeline after first release. Uncomment lines below and update Zenodo doi and badge at the top of this file. -->
If you use nf-core/magmap for your analysis, please cite it using the following doi: [10.5281/zenodo.XXXXXX](https://doi.org/10.5281/zenodo.XXXXXX)

An extensive list of references for the tools used by the pipeline can be found in the [`CITATIONS.md`](CITATIONS.md) file.

You can cite the `nf-core` publication as follows:

> **The nf-core framework for community-curated bioinformatics pipelines.**
>
> Philip Ewels, Alexander Peltzer, Sven Fillinger, Harshil Patel, Johannes Alneberg, Andreas Wilm, Maxime Ulysse Garcia, Paolo Di Tommaso & Sven Nahnsen.
>
> _Nat Biotechnol._ 2020 Feb 13. doi: [10.1038/s41587-020-0439-x](https://dx.doi.org/10.1038/s41587-020-0439-x).
