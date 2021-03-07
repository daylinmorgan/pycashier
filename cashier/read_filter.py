import os
import csv
from pathlib import Path


def filter_by_percent(file_in, filter_percent):

    total_reads = 0

    with open(file_in, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            total_reads += float(row[1])

    filter_count = int(round(total_reads * filter_percent / 100, 0))

    filter_by_count(file_in, filter_count)


def filter_by_count(file_in, filter_count):

    name = file_in.stem
    ext = file_in.suffix
    csv_out = Path('outs') / f'{name}.min{filter_count}{ext}'
    total_reads = 0

    with open(file_in, 'r') as csv_in:
        with open(csv_out, 'w') as csv_out:
            for line in csv_in:
                linesplit = line.split('\t')
                if int(linesplit[1]) >= filter_count:
                    csv_out.write(u'{}\t{}'.format(*linesplit))


def read_filter(sample, filter_count, filter_percent, quality, ratio, distance,
                **kwargs):

    file_in = Path('pipeline') / f'{sample}.barcodes.q{quality}.r{ratio}d{distance}.tsv'

    if filter_count:
        print('\nremoving sequences with less than {} total occurences'.format(
            filter_count))
        filter_by_count(file_in, filter_count)

    else:
        print(
            '\nremoving sequences with less than {}% of the total reads per sample'
            .format(filter_percent))
        filter_by_percent(file_in, filter_percent)
