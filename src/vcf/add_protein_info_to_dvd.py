import os
import pandas as pd
import traceback
import src.utils as utils
from importlib import reload
import zipfile

split_chroms_dir_path = 'split_vcf_chromosomes_csvs_compressed'
split_chroms_dir = os.listdir(split_chroms_dir_path)

for file in split_chroms_dir:
    utils.extract_tarball(os.path.join(split_chroms_dir_path, file))


import re
ddg_data_correction_pattern = r"\{[^}]*\}(?:,)?"

# with open('unzipped/merged_DDGData.csv', 'r') as ddg_file:
#     with open('corrected_merged_DDGData.csv', 'w') as corrected_file:
#         for line in ddg_file.readlines():
#             loc = re.search(line, ddg_data_correction_pattern)
#             if loc is not None:
#                 new_line = line[:loc.start()] + line[loc.end():]
#                 print('here')
#                 break
#             else:
#                 new_line = line
#             corrected_file.write(new_line)
            


# df = pd.read_csv('unzipped/merged_DDGData.csv')
# df = pd.read_csv('merged_DDGData.csv')

# Unzipping archive containing DDG data
with zipfile.ZipFile('DVD_csvs.zip') as dvd_csvs:
    dvd_csvs.extractall()

# Removing the applied filter line from all the gene files
csvs = [os.path.join('featureMappedCsvs', c) for c in os.listdir('featureMappedCsvs')]
for csv in csvs:
    with open(csv, 'r') as file:
        lines = file.readlines()[1:]
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
    df[index_cols] = pd.DataFrame(df.loc[:, 'Genomic Description (GRCh37)'].apply(split_genomic_description).tolist(), index=df.index)

ddg_df = pd.concat(dfs)
ddg_df = ddg_df.set_index(index_cols)


df = pd.read_csv('extracted_files/split_vcf_chromosomes_csvs/chromosome_12_records.csv', index_col=0)
df.ALT[0]
df.ALT.dtype
df.ALT.astype(vcfpy.Record)
df['TYPE'] = df.ALT.apply(lambda x: x[0].type)
df['ALT'] = df.ALT.apply(lambda x: x[0].value)

df = df.set_index(index_cols)
df.index

# for idx in ddg_df.index:

i = ddg_df.index[0]
ddg_df.loc[i]
df.loc[i]
