import sys
import shlex
import subprocess
from pathlib import Path

from .utils import sam_to_name_labeled_fastq, labeled_fastq_to_tsv
from .console import console


####
from time import sleep

####
def single_cell_process(sample, f, sourcedir, cli_args,status):
    # print(f'performing barcode extraction on sample: {sample}')
    console.log(
            f'[green]{sample}[/green]: extracting barcodes')

    error_rate = cli_args['extract']['error_rate']
    threads = cli_args['main']['threads']
    barcode_length_min = 10
    barcode_length = cli_args['extract']['barcode_length']
    upstream_adapter = cli_args['extract']['upstream_adapter']
    downstream_adapter = cli_args['extract']['downstream_adapter']
    adapter_string = f'-g {upstream_adapter} -a {downstream_adapter}'

    input_file = f
    pipeline_dir = Path('pipeline')
    fastq_out = pipeline_dir / f"{sample}.cell_record_labeled.fastq"
    output_file = pipeline_dir / f"{sample}.cell_record_labeled.barcode.fastq"
    tsv_out = Path('outs') / f'{sample}.cell_record_labeled.barcode.tsv'

    if not fastq_out.is_file():
        console.log(f'[green]{sample}[/green]: converting sam to labeled fastq')
        status.stop()
        sam_to_name_labeled_fastq(sample, input_file, fastq_out)
        status.start()
    else:
        console.log(f'[green]{sample}[/green]: skipping sam to labeled fastq conversion')

    if not output_file.is_file():

        # print(f'Performing extraction on sample: {sample}')
        console.log(
            f'[green]{sample}[/green]: extracting barcodes')

        command = f'cutadapt -e {error_rate} -j {threads} --minimum-length={barcode_length_min} --maximum-length={barcode_length} --max-n=0 --trimmed-only {adapter_string} -n 2 -o {output_file} {fastq_out}'
        args = shlex.split(command)

        p = subprocess.run(args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True)

        if cli_args['main']['verbose']:
            console.print('[yellow]CUTADAPT OUTPUT:')
            console.print(p.stdout)

    if not tsv_out.is_file():
        console.log(f'[green]{sample}[/green]: converting labeled fastq to tsv')
        labeled_fastq_to_tsv(output_file, tsv_out)
        
    else:
        console.log(
            f'[green]{sample}[/green]: skipping labeled fastq to tsv conversion')




    # print(f'Completed barcode extraction for sample: {sample}')


def single_cell(sourcedir, cli_args):

    console.rule('SINGLE CELL MODE',align='center',style='red')
    print()

    sam_files = [f for f in sourcedir.iterdir()]

    for f in sam_files:

        ext = f.suffix

        if ext != '.sam':
            raise ValueError('There is a non sam file in the provided input directory:')

    for f in sam_files:

        sample = f.name.split('.')[0]

        with console.status(f"Processing sample: [green]{sample}[/green]",
                                    spinner='dots12') as status:
            sleep(5)
            single_cell_process(sample, f, sourcedir, cli_args, status)

        console.log(f'[green]{sample}[/green]: processing completed')
        console.rule()
        
    # print('\nfinished extracting barcodes from sam files')
    # print('exiting.')
    console.print('\n[green]FINISHED!')
    exit()
