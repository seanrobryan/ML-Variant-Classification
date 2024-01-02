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
chromosomes = []
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
            chromosomes.append(cur_vcf_chromosome)
        except Exception as e:
            logging.error(traceback.format_exc())
            print(f"\nSkipping chromosome {chromosome}")


reader = vcfpy.Reader.from_path(dvd_gz, tabix_path=dvd_gz_index)

mt_records = reader.fetch('MT')
# mt_records = [r for r in mt_records]
mt_chromosome = VCFChromosome('MT')
mt_chromosome.add_records(mt_records)
mt_chromosome.update_dataframe()
mt_df = mt_chromosome.df.copy()

mt_df['TYPE'] = mt_df.ALT.apply(lambda x: x[0].type)
mt_df['ALT'] = mt_df.ALT.apply(lambda x: x[0].value)

cols = mt_df.columns.tolist()
new_col_order = cols[0:4] + [cols[-1], 'GENE'] + [c for c in cols[4:-1] if c != 'GENE']
mt_df = mt_df[new_col_order]

domainsToEditWithClass_df = pd.read_csv('inputs/domainsToEditWithClass.csv', index_col=0)
domainsToEditWithClass_df.head()

merged_csv_wConfidence_df = pd.read_csv('inputs/merged_csv_wConfidence.csv')
merged_csv_wConfidence_df.head()

merged_csv_wFreeEnergies_df = pd.read_csv('inputs/merged_csv_wFreeEnergies.csv') 
merged_csv_wFreeEnergies_df.head()

reader.INFO



# df = pd.read_csv('zips/merged_DDGData.csv', low_memory=False)

# 'modified_merged_DDGData.csv'

pd.read_csv('unzipped/merged_DDGData.csv')
pd.read_csv('unzipped/featureMappedCsvs/merged_DDGData.csv')

ddg_data_correction_pattern = r'\{[^}]*\}(?:,)?'
import re

with open('unzipped/featureMappedCsvs/merged_DDGData.csv', 'r') as ddg_file:
    with open('corrected_merged_DDGData.csv', 'w') as corrected_file:
        for line in ddg_file.readlines():
            loc = re.search(line, ddg_data_correction_pattern)
            if loc is not None:
                new_line = line[:loc.start()] + line[loc.end():]
            else:
                new_line = line
            corrected_file.write(new_line+'\n')
