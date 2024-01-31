import vcfpy
import pandas as pd
from importlib import reload
import src.utils as utils
from src.vcf.VCFChromosome import VCFChromosome
import os
import sys

import traceback
import logging
import warnings

chroms_names = ['MT', 'X'] + [str(x) for x in range(1,23)]
GENOMIC_DESCRIPTION_COL = 'Genomic Description (GRCh37)'

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

def separate_chromosomes_from_dvd_vcf(dvd_gz, dvd_gz_index, chromosome_dir='split_vcf_chromosomes_csvs'):
    if not os.path.isdir(chromosome_dir):
        os.makedirs(chromosome_dir)
    
    reader = vcfpy.Reader.from_path(dvd_gz, tabix_path=dvd_gz_index)
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

separate_chromsomes_from_dvd_vcf(dvd_gz, dvd_gz_index, 'split_vcf_chromosomes_csvs')

# chromosome_dir = 'split_vcf_chromosomes_csvs'
# if not os.path.isdir(chromosome_dir):
#     os.makedirs(chromosome_dir)

# reader = vcfpy.Reader.from_path(dvd_gz, tabix_path=dvd_gz_index)
# chromosomes = {}
# problematic_records = []
# for chromosome in chroms_names:
#     # if chromosome not in ['10']: continue
#     file = f"chromosome_{chromosome}_records.csv"
#     if os.path.isfile(file):
#         print(f"{file} already existings...moving to next chromosome")
#     else:
#         try:
#             print("Current chromosome:", chromosome)
#             chromosome_records = reader.fetch(chromosome)
#             cur_vcf_chromosome = VCFChromosome(chromosome)
#             cur_vcf_chromosome.add_records(chromosome_records) # Error occuring here
#             cur_vcf_chromosome.update_dataframe()
            
#             fname = os.path.join(chromosome_dir, f"chromosome_{chromosome}_records")
#             cur_vcf_chromosome.df.to_csv(fname + '.csv')
#             chromosomes[chromosome] = cur_vcf_chromosome
#         except Exception as e:
#             logging.error(traceback.format_exc())
#             print(f"\nSkipping chromosome {chromosome}")



for c in chroms_names:
    utils.extract_tarball(os.path.join(compressed_dir, f"chromosome_{c}_records.tar.gz"))

# # Removing the applied filter line from all the gene files
# feature_mapped_csv_dir = os.path.join('unzipped', 'featureMappedCsvs')
# csvs = [os.path.join(feature_mapped_csv_dir, c) for c in os.listdir(feature_mapped_csv_dir)]
# dfs = []
# for csv in csvs:
#     with open(csv, 'r') as file:
#         lines = file.readlines()
#         if lines[0].startswith('{'):
#             lines = lines[1:]
#     with open(csv, 'w') as file:
#         file.writelines(lines)
#     dfs.append(pd.read_csv(csv))
        
# dfs = []
# for csv in csvs:
#     dfs.append(pd.read_csv(csv))


def split_genomic_description(genomic_description):
    chromosome, position, change = genomic_description.split(':')
    ref, alt = change.split('>')
    return chromosome, ref, alt, position

def add_genomic_description_cols(df, set_as_index = True):
    index_cols = ['CHROM', 'REF', 'ALT', 'POS']
    df[index_cols] = pd.DataFrame(df.loc[:, GENOMIC_DESCRIPTION_COL].apply(split_genomic_description).tolist())
    df.set_index(GENOMIC_DESCRIPTION_COL, inplace=True)
    return df

# index_cols = ['CHROM', 'REF', 'ALT', 'POS']
# for df in dfs:
#     df[index_cols] = pd.DataFrame(df.loc[:, new_index_col].apply(split_genomic_description).tolist(), index=df.index)
    
# ddg_df = add_genomic_description_cols(pd.concat(dfs), set_as_index=True)
# # ddg_df.set_index(new_index_col, inplace=True)
# ddg_merged_file = 'merged_feature_mapped_ddg_values.csv'
# ddg_df.to_csv(ddg_merged_file)
 
# compressed_chrom_w_ddg_dir = 'compressed_chromosome_w_ddg/'
# if not os.path.isdir(compressed_chrom_w_ddgo_dir):
#     os.makedirs(compressed_chrom_w_ddg_dir)

def merge_ddg_dvd_dfs(ddg_file_name, chromosome_dir, save_files_to_dir):
    # chromosome_ddg_dir = 'chromosomes_w_ddg'
    if not os.path.isdir(save_files_to_dir):
        os.makedirs(save_files_to_dir)
    merged_dfs = {}
    ddg_df = pd.read_csv(ddg_file_name, index_col=0)
    old_index_col = 'Genomic Description GRCh37'
    new_index_col = 'Genomic Description (GRCh37)'

    for chrom in chroms_names:
        try:
            cur_chrom_df = pd.read_csv(f"{chromosome_dir}/chromosome_{chrom}_records.csv", index_col=0)
            cur_chrom_df.rename(columns={old_index_col: new_index_col}, inplace=True)
            cur_chrom_df.set_index(new_index_col, inplace=True)
            merged_dfs[chrom] = cur_chrom_df.merge(ddg_df, left_index=True, right_index=True, how='inner')
        
            chrom_w_ddg_file = os.path.join(save_files_to_dir, f"chromosome_{chrom}_w_ddg.csv")
            merged_dfs[chrom].to_csv(chrom_w_ddg_file)
            
            # # Archived csv
            # archived_csv = os.path.join(compressed_chrom_w_ddg_dir, os.path.splitext(os.path.basename(chrom_w_ddg_file))[0] + '.tar')
            # utils.archive_files(chrom_w_ddg_file, archived_csv)

            # # Compress archive
            # compressed_archive = archived_csv + '.gz'
            # utils.compress(archived_csv, compressed_archive)

            # os.remove(chrom_w_ddg_file)
            # os.remove(archived_csv)

        except Exception as e:
            print(e)

ddg_merged_file = "merged_feature_mapped_ddg_values.csv"
chromosome_ddg_dir = 'chromosomes_w_ddg'
merge_ddg_dvd_dfs(ddg_file_name=ddg_merged_file, chromosome_dir='split_vcf_chromosomes_csvs', save_files_to_dir='chromosomes_w_ddg')
utils.compress_directory_contents_to_tarballs(directory='chromosomes_w_ddg', decompress_to='compressed_chromosome_w_ddg', remove_dir=True)
os.removedirs(chromosome_ddg_dir)


def main(args):
    # dvd_vcf_gzipped = args[1] # /home/srryn/hpchome/DVD/versions/9_1_1/final_outputs/delete_later/DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz
    # dvd_vcf_index_gzipped = args[2] # /home/srryn/hpchome/DVD/versions/9_1_1/final_outputs/delete_later/DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz.tbi
    # feature_mapped_csv_dir = args[3] # /unzipped/featureMappedCsvs/
    # ddg_merged_file = args[4] # merged_feature_mapped_ddg_values.csv
    dvd_vcf_gzipped = "DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz"
    dvd_vcf_index_gzipped = "DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz.tbi"
    feature_mapped_csv_dir = "featureMappedCsvs"
    ddg_merged_file = "merged_feature_mapped_ddg_values.csv"

    vcf_chromosome_dir = 'split_vcf_chromosomes_csvs'
    compressed_vcf_chromosome_dir = vcf_chromosome_dir + '_compressed'

    # Extract contents of DVD .vcf and create separate 
    separate_chromosomes_from_dvd_vcf(dvd_vcf_gzipped, dvd_vcf_index_gzipped, vcf_chromosome_dir)

    # Compress individual chromosome csvs to tarballs
    utils.compress_directory_contents_to_tarballs(directory=vcf_chromosome_dir, decompress_to=compressed_vcf_chromosome_dir, remove_dir=True)

    # Decompressed files were previously remove, re-extract the tarballs here
    for c in chroms_names:
        utils.extract_tarball(os.path.join(compressed_vcf_chromosome_dir, f"chromosome_{c}_records.tar.gz"))

    # Removing the applied filter line from all the gene files
    csvs = [os.path.join(feature_mapped_csv_dir, c) for c in os.listdir(feature_mapped_csv_dir)]
    dfs = []
    for csv in csvs:
        with open(csv, 'r') as file:
            lines = file.readlines()
            if lines[0].startswith('{'):
                lines = lines[1:]
        with open(csv, 'w') as file:
            file.writelines(lines)
        dfs.append(pd.read_csv(csv))
            
    ddg_df = add_genomic_description_cols(pd.concat(dfs), set_as_index=True)
    # ddg_df.set_index(new_index_col, inplace=True)
    ddg_df.to_csv(ddg_merged_file)
    
    # Merge DDG values with DVD .vcf files
    merge_ddg_dvd_dfs(ddg_file_name=ddg_merged_file, chromosome_dir=vcf_chromosome_dir, save_files_to_dir='chromosomes_w_ddg')
    utils.compress_directory_contents_to_tarballs(directory='chromosomes_w_ddg', decompress_to='compressed_chromosome_w_ddg', remove_dir=True)

if __name__ == '__main__':
    main(sys.argv)