
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'genomeinfo': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to comma-separated file containing information about the genomes.',
    ),
    'gtdbtk_metadata': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to comma-separated file containing the output from gtdbtk.',
    ),
    'ncbi_genome_infos': NextflowParameter(
        type=typing.Optional[str],
        default='./assets/ncbi_genome_infos.csv',
        section_title=None,
        description='Path to txt file with information about genomes in nbci.',
    ),
    'indexes': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to .sbt file.',
    ),
    'gtdb_metadata': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to comma-separated file containing information from gtdb.',
    ),
    'checkm_metadata': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to comma-separated file containing the output from CheckM.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'skip_qc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Quality control options',
        description='Skip all QC steps except for MultiQC.',
    ),
    'skip_fastqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip FastQC.',
    ),
    'clip_r1': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Trimming options',
        description="Instructs Trim Galore to remove bp from the 5' end of read 1 (or single-end reads).",
    ),
    'clip_r2': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 5' end of read 2 (or single-end reads).",
    ),
    'three_prime_clip_r1': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 3' end of read 1 AFTER adapter/quality trimming has been performed.",
    ),
    'three_prime_clip_r2': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Instructs Trim Galore to remove bp from the 3' end of read 2 AFTER adapter/quality trimming has been performed.",
    ),
    'trim_nextseq': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Instructs Trim Galore to apply the --nextseq=X option, to trim based on quality after removing poly-G tails.',
    ),
    'save_trimmed': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the trimmed FastQ files in the results directory.',
    ),
    'skip_trimming': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip the adapter trimming step.',
    ),
    'sequence_filter': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='BBtools options',
        description='Instructs BBduk to use a fasta file to filter away sequences before running further analysis.',
    ),
    'bbmap_minid': NextflowParameter(
        type=typing.Optional[float],
        default=0.9,
        section_title=None,
        description='Minimal identity for BBmap',
    ),
    'save_bam': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save bam output file',
    ),
    'sourmash': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Sourmash',
        description='Activate Sourmash',
    ),
    'ksize': NextflowParameter(
        type=typing.Optional[int],
        default=21,
        section_title=None,
        description='K-mer size used by Sourmash',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

