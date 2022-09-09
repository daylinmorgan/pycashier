from .term import term
from .utils import get_filter_count


def filter_by_percent(file_in, filter_percent, length, offset, outdir):

    filter_by_count(
        file_in, get_filter_count(file_in, filter_percent), length, offset, outdir
    )


def filter_by_count(file_in, filter_count, length, offset, output):

    name = file_in.stem
    ext = file_in.suffix
    final = output / f"{name}.min{filter_count}_off{offset}{ext}"

    with open(file_in, "r") as csv_in:
        with open(final, "w") as csv_out:
            for line in csv_in:
                linesplit = line.split("\t")
                if (
                    int(linesplit[1]) >= filter_count
                    and abs(len(linesplit[0]) - length) <= offset
                ):
                    csv_out.write(f"{linesplit[0]}\t{linesplit[1]}")

    if final.stat().st_size == 0:
        term.print(
            "[yellow]WARNING[/]: no barcodes passed final length and abundance filters"
        )


def read_filter(
    sample,
    pipeline,
    output,
    length,
    offset,
    filter,
    quality,
    ratio,
    distance,
):
    file_in = pipeline / f"{sample}.q{quality}.barcodes.r{ratio}d{distance}.tsv"

    if "filter_count" in filter.keys():
        term.print(
            f"[green]{sample}[/green]: removing "
            f"sequences with less than [hl]{filter['filter_count']}[/hl] reads"
        )

        filter_by_count(file_in, filter["filter_count"], length, offset, output)

    else:
        term.print(
            f"[green]{sample}[/green]: removing"
            f" sequences with less than [hl]{filter['filter_percent']}%[/hl] of total reads"
        )

        filter_by_percent(file_in, filter["filter_percent"], length, offset, output)
