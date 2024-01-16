import vcfpy
import pandas as pd
from importlib import reload
import src.utils as utils
from src.vcf.VCFChromosome import VCFChromosome
import os

import traceback
import logging

dvd_dir = '/Users/seanryan/Documents/School/Graduate/Variant_Classification_Braun/files_from_MORL_argon/DVD/9_1_1/final_output/'
morl_dvd_dir = '/home/srryn/hpchome/DVD/versions/9_1_1/final_outputs/'


active_dir = morl_dvd_dir

active_dir = os.path.join(active_dir, 'delete_later')

# Open file, this will read in the header
# dvd_file = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf')
'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf'
# dvd_file = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf')
# dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes.vcf.gz')
# dvd_bgz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf.bgz')

# dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf.gz')


dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz')
dvd_gz_index = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz.tbi')

chromosome_dir = 'split_vcf_chromosomes_csvs'
if not os.path.isdir(chromosome_dir):
    os.makedirs(chromosome_dir)

reader = vcfpy.Reader.from_path(dvd_gz, tabix_path=dvd_gz_index)
chroms_names = ['MT', 'X'] + [str(x) for x in range(1,23)]
chromosomes = {}
problematic_records = []
for chromosome in chroms_names:
    # if chromosome not in ['10']: continue
    file = f"chromosome_{chromosome}_records.csv"
    if os.path.isfile(file):
        print(f"{file} already existings...moving to next chromosome")
    else:
        try:
            print("Current chromosome:", chromosome)
            chromosome_records = reader.fetch(chromosome)
            cur_vcf_chromosome = VCFChromosome(chromosome)
            cur_vcf_chromosome.add_records(chromosome_records) # Error occuring here
            cur_vcf_chromosome.update_dataframe()
            
            fname = os.path.join(chromosome_dir, f"chromosome_{chromosome}_records")
            cur_vcf_chromosome.df.to_csv(fname + '.csv')
            chromosomes[chromosome] = cur_vcf_chromosome
        except Exception as e:
            logging.error(traceback.format_exc())
            print(f"\nSkipping chromosome {chromosome}")


from importlib import reload
reload(utils)
compressed_dir = 'split_vcf_chromosomes_csvs_compressed'
if not os.path.isdir(compressed_dir):
    os.mkdir(compressed_dir)

for chromosome_csv in os.listdir(chromosome_dir):
    chromosome_csv = os.path.join(chromosome_dir, chromosome_csv)

    # Archived csv
    archived_csv = os.path.join(compressed_dir, os.path.splitext(os.path.basename(chromosome_csv))[0] + '.tar')
    utils.archive_files(chromosome_csv, archived_csv)

    # Compress archive
    compressed_archive = archived_csv + '.gz'
    utils.compress(archived_csv, compressed_archive)
    
    os.remove(chromosome_csv)
    os.remove(archived_csv)


os.removedirs(chromosome_dir)

for c in chroms_names:
    utils.extract_tarball(os.path.join(compressed_dir, f"chromosome_{c}_records.tar.gz"))

old_index_col = 'Genomic Description GRCh37'
new_index_col = 'Genomic Description (GRCh37)'

# Removing the applied filter line from all the gene files
feature_mapped_csv_dir = os.path.join('unzipped', 'featureMappedCsvs')
csvs = [os.path.join(feature_mapped_csv_dir, c) for c in os.listdir(feature_mapped_csv_dir)]
for csv in csvs:
    with open(csv, 'r') as file:
        lines = file.readlines()
        if lines[0].startswith('{'):
            lines = lines[1:]
    with open(csv, 'w') as file:
        file.writelines(lines)
        
dfs = []
for csv in csvs:
    dfs.append(pd.read_csv(csv))


def split_genomic_description(genomic_description):
    chromosome, position, change = genomic_description.split(':')
    ref, alt = change.split('>')
    return chromosome, ref, alt, position

index_cols = ['CHROM', 'REF', 'ALT', 'POS']
for df in dfs:
    df[index_cols] = pd.DataFrame(df.loc[:, new_index_col].apply(split_genomic_description).tolist(), index=df.index)

ddg_df = pd.concat(dfs)
ddg_df.set_index(new_index_col, inplace=True)
ddg_merged_file = 'merged_feature_mapped_ddg_values.csv'
ddg_df.to_csv(ddg_merged_file)

chromosome_ddg_dir = 'chromosomes_w_ddg'
os.mkdir(chromosome_ddg_dir)

merged_dfs = {}
ddg_df = pd.read_csv(ddg_merged_file, index_col=0)
for chrom in chroms_names:
    try:
        cur_chrom_df = pd.read_csv(f"extracted_files/split_vcf_chromosomes_csvs/chromosome_{chrom}_records.csv", index_col=0)
        cur_chrom_df.rename(columns={old_index_col: new_index_col}, inplace=True)
        cur_chrom_df.set_index(new_index_col, inplace=True)
        merged_dfs[chrom] = cur_chrom_df.merge(ddg_df, left_index=True, right_index=True, how='inner')

        merged_dfs[chrom].to_csv(f"chromosomes_w_ddg/chromosome_{chrom}_w_ddg.csv")
    except Exception as e:
        print(e)

