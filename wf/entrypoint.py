from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, genomeinfo: typing.Optional[str], gtdbtk_metadata: typing.Optional[str], indexes: typing.Optional[str], gtdb_metadata: typing.Optional[str], checkm_metadata: typing.Optional[str], email: typing.Optional[str], multiqc_title: typing.Optional[str], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], skip_qc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], clip_r1: typing.Optional[str], clip_r2: typing.Optional[str], three_prime_clip_r1: typing.Optional[str], three_prime_clip_r2: typing.Optional[str], trim_nextseq: typing.Optional[str], save_trimmed: typing.Optional[bool], skip_trimming: typing.Optional[bool], sequence_filter: typing.Optional[str], save_bam: typing.Optional[bool], sourmash: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], ncbi_genome_infos: typing.Optional[str], bbmap_minid: typing.Optional[float], ksize: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('genomeinfo', genomeinfo),
                *get_flag('gtdbtk_metadata', gtdbtk_metadata),
                *get_flag('ncbi_genome_infos', ncbi_genome_infos),
                *get_flag('indexes', indexes),
                *get_flag('gtdb_metadata', gtdb_metadata),
                *get_flag('checkm_metadata', checkm_metadata),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('outdir', outdir),
                *get_flag('skip_qc', skip_qc),
                *get_flag('skip_fastqc', skip_fastqc),
                *get_flag('clip_r1', clip_r1),
                *get_flag('clip_r2', clip_r2),
                *get_flag('three_prime_clip_r1', three_prime_clip_r1),
                *get_flag('three_prime_clip_r2', three_prime_clip_r2),
                *get_flag('trim_nextseq', trim_nextseq),
                *get_flag('save_trimmed', save_trimmed),
                *get_flag('skip_trimming', skip_trimming),
                *get_flag('sequence_filter', sequence_filter),
                *get_flag('bbmap_minid', bbmap_minid),
                *get_flag('save_bam', save_bam),
                *get_flag('sourmash', sourmash),
                *get_flag('ksize', ksize),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_magmap", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_magmap(input: LatchFile, genomeinfo: typing.Optional[str], gtdbtk_metadata: typing.Optional[str], indexes: typing.Optional[str], gtdb_metadata: typing.Optional[str], checkm_metadata: typing.Optional[str], email: typing.Optional[str], multiqc_title: typing.Optional[str], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], skip_qc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], clip_r1: typing.Optional[str], clip_r2: typing.Optional[str], three_prime_clip_r1: typing.Optional[str], three_prime_clip_r2: typing.Optional[str], trim_nextseq: typing.Optional[str], save_trimmed: typing.Optional[bool], skip_trimming: typing.Optional[bool], sequence_filter: typing.Optional[str], save_bam: typing.Optional[bool], sourmash: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], ncbi_genome_infos: typing.Optional[str] = './assets/ncbi_genome_infos.csv', bbmap_minid: typing.Optional[float] = 0.9, ksize: typing.Optional[int] = 21) -> None:
    """
    nf-core/magmap

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, genomeinfo=genomeinfo, gtdbtk_metadata=gtdbtk_metadata, ncbi_genome_infos=ncbi_genome_infos, indexes=indexes, gtdb_metadata=gtdb_metadata, checkm_metadata=checkm_metadata, email=email, multiqc_title=multiqc_title, outdir=outdir, skip_qc=skip_qc, skip_fastqc=skip_fastqc, clip_r1=clip_r1, clip_r2=clip_r2, three_prime_clip_r1=three_prime_clip_r1, three_prime_clip_r2=three_prime_clip_r2, trim_nextseq=trim_nextseq, save_trimmed=save_trimmed, skip_trimming=skip_trimming, sequence_filter=sequence_filter, bbmap_minid=bbmap_minid, save_bam=save_bam, sourmash=sourmash, ksize=ksize, multiqc_methods_description=multiqc_methods_description)

