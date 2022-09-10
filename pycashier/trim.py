import shutil

from .term import term
from .utils import fastq_to_csv, run_cmd


def trim(
    sample,
    pipeline,
    fastq,
    quality,
    unqualified_percent,
    fastp_args,
    error,
    threads,
    length,
    distance,
    upstream_adapter,
    downstream_adapter,
    unlinked_adapters,
    skip_trimming,
    verbose,
    status,
):

    json, html = (pipeline / "qc" / f"{sample}.{ext}" for ext in ("json", "html"))
    filtered_fastq, filtered_barcode_fastq = (
        pipeline / "qc" / f"{sample}.q{quality}.{ext}"
        for ext in ("fastq", "barcode.fastq")
    )

    adapter_string = (
        f"-g {upstream_adapter} -a {downstream_adapter}"
        if unlinked_adapters
        else f"-g {upstream_adapter}...{downstream_adapter}"
    )

    (pipeline / "qc").mkdir(exist_ok=True)

    if not filtered_fastq.is_file():

        term.process("quality filtering reads w/ [b]fastp[/]")
        command = (
            "fastp "
            f"-i {fastq} "
            f"-o {filtered_fastq} "
            f"-q {quality} "
            f"-u {unqualified_percent} "
            f"-w {threads} "
            f"-h {html} "
            f"-j {json} "
            "--dont_eval_duplication "
            f"{fastp_args or ''}"
        )

        run_cmd(command, sample, filtered_fastq, verbose, status)

    if skip_trimming:
        shutil.copy(filtered_fastq, filtered_barcode_fastq)

    if not filtered_barcode_fastq.is_file():

        term.process("extracting barcodes w/ [b]cutadapt[/]")

        command = (
            "cutadapt "
            f"-e {error} "
            f"-j {threads} "
            f"--minimum-length={length - distance} "
            f"--maximum-length={length + distance} "
            f"--max-n=0 "
            f"--trimmed-only "
            f"{adapter_string} "
            f"-n 2 "
            f"-o {filtered_barcode_fastq} {filtered_fastq}"
        )

        run_cmd(command, sample, filtered_barcode_fastq, verbose, status)
        term.process("filtering and extraction complete")

    else:
        term.process("skipping extraction")

    barcodes_out = pipeline / f"{sample}.q{quality}.barcodes.tsv"

    if not barcodes_out.is_file():
        term.process("converting fastq to tsv")
        fastq_to_csv(filtered_barcode_fastq, barcodes_out)
    else:
        term.process("skipping fastq to tsv conversion")
