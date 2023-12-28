print('CHROM POS gnomad_MAX_MAF_SOURCE')


# chrom_4_records = reader.fetch('1')
# for record in chrom_4_records:
chrom_count = {}
for record in reader:
    if record.CHROM in chrom_count:
        chrom_count[record.CHROM] += 1
    else:
        chrom_count[record.CHROM] = 1
    dvd_count += 1
    if dvd_count % 10000 == 0:
        print(dvd_count)

print(chrom_count)

rows = []
dvd_count = 0
non_snv_count = 0
record_of_interest = None
reader = vcfpy.Reader.from_path(dvd_file)
print('CHROM POS gnomad_MAX_MAF_SOURCE')

chromosomes = ['MT', 'X'] + [x for x in range(1,24)]

# chrom_4_records = reader.fetch('4')
# for record in chrom_4_records:
#     dvd_count += 1
#     if dvd_count % 10000 == 0:
#         print(dvd_count)


def subset_vcf(input_file, output_file, n_lines):
    # Made a new txt (vcf) file from the first n_lines lines of the dvd vcf to look at it manually
    with open(input_file, 'r') as dvd:
        with open(output_file, 'w') as out_file:
            for i in range(0, n_lines):
                l = dvd.readline()
                out_file.write(l)

# subset_vcf(dvd_file, 'dvd_subset.txt', 2500)

# def terry_method():
#     reader = vcfpy.Reader.from_path(dvd_bgz)
    
#     # Build and print header
#     header = ['#CHROM', 'POS', 'REF', 'ALT'] + reader.header.samples.names

#     dvd_count = 0
#     non_snv_count = 0

#     print("dvd_chr dvd_pos_dvd_state dvd_key ")

#     info_field_lens = {}
#     info_fields = []
#     unique_info_fields = set()

#     for record in reader:
#         # this must skip all non-SNVs
#         if not record.is_snv():
#             non_snv_count=non_snv_count+1
#             continue
        
#         dvd_count=dvd_count+1
        
#         dvd_chr = record.CHROM
#         dvd_pos = record.POS
#         dvd_ref = record.REF
#         dvd_alt = record.ALT
#         dvd_info = record.INFO
        
#         info_len = len(dvd_info)

#         if info_len in info_field_lens.keys():
#             info_field_lens[info_len] = info_field_lens[info_len] + 1
#         else:
#             info_field_lens[info_len] = 1


#         unique_info_fields.update(dvd_info.keys())
#         info_fields.append([x for x in dvd_info.keys()])
        
#         # creating a list
#         # really only expect 1 ALT
#         alts = []
#         alts = alts + [alt.value for alt in record.ALT]
#         alts = alts + [call.data.get('GT') or './.' for call in record.calls]

#         # this assumes only 1 ALT allele
#         dvd_alt = alts[0]

#         dvd_key = str(dvd_chr) + str(dvd_pos)+str(dvd_ref)+str(dvd_alt)

#         #if(hasattr(record, "INFO"):
#         if( "FINAL_PATHOGENICITY" in record.INFO):
#             dvd_state = record.INFO["FINAL_PATHOGENICITY"]
#         else:
#             print("did not find INFO field in DVD")
#             exit()

#         # convert from a list to a string
#         dvd_state = str(dvd_state)

#         # I think I have to do this because it is a list?
#         # remove first 2 and last 2 chars
#         # Just pull out the first time from the list ********
#         dvd_state=dvd_state[2:]
#         dvd_state=dvd_state[:-2]


#         dvd_state = dvd_state.lower()
#         if 'benign' in dvd_state: dvd_state = 'benign'
#         elif 'pathogenic' in dvd_state: dvd_state = 'pathogenic'
#         elif 'unknown' in dvd_state: dvd_state = 'ambiguous'
#         else: print("error dvd dvd_state", dvd_state)

#         if dvd_pos % 1000 == 0:
#             # print("dvd_chr dvd_pos_dvd_state dvd_key ",dvd_chr,dvd_pos,dvd_state,dvd_key)
#             print(dvd_chr,dvd_pos,dvd_state,dvd_key)

#         #print("dvd_state = ",dvd_state)
#         #print("dvd_key = ",dvd_key)
        
        
#     with open('info_field_counts.txt', 'w') as f:
#         for k, v in info_field_lens.items():
#             f.write(f"{k},{v}\n")
        
        
#     df = pd.DataFrame(info_fields).to_csv('info_fields.csv')


# df = pd.read_csv('info_fields.csv', index_col=0)
# df_backup = df.copy()
# df = df.dropna()
# df

# unique_values = df.stack().unique()
# unique_values
# len(unique_values)


# output_df = pd.DataFrame([], columns=header + unique_values.tolist())
rows = []
dvd_count = 0
non_snv_count = 0
record_of_interest = None
reader = vcfpy.Reader.from_path(dvd_file)
print('CHROM POS gnomad_MAX_MAF_SOURCE')


chrom_4_records = reader.fetch('4')
for record in chrom_4_records:
    dvd_count += 1
    if dvd_count % 10000 == 0:
        print(dvd_count)

rows = []
dvd_count = 0
non_snv_count = 0
record_of_interest = None
reader = vcfpy.Reader.from_path(dvd_bgz)
for record in reader:
    # this must skip all non-SNVs
    if not record.is_snv():
        non_snv_count=non_snv_count+1
        continue
    
    dvd_count=dvd_count+1

    dvd_chr, dvd_pos, dvd_ref, dvd_alt, dvd_info = record.CHROM, record.POS, record.REF, record.ALT, record.INFO

    # Initalize the new dataframe row with all None
    # new_row_dict = {k:None for k in output_df.columns.tolist()}
    new_row_dict = {}
    
    for c, v in zip(['#CHROM', 'POS', 'REF', 'ALT'], [dvd_chr, dvd_pos, dvd_ref, dvd_alt, dvd_info]):
        new_row_dict[c] = v
    
    for key, value in dvd_info.items():
        if isinstance(value, list):
            if len(value) == 0:
                value = None
                new_row_dict[key] = value
            elif len(value) == 1:
                value = value[0]
                new_row_dict[key] = value
            # elif len(value) > 1:
                
            else:
                record_of_interest = record
                value = ','.join(value)
                # longer.append(value)
                # print(f'index: {dvd_count}')
                # print(f'Value {value} of unexpected length {len(value)} encountered at key {key}')
    # try:
    #     gnomad_max_maf_source = record.INFO['gnomad_MAX_MAF_SOURCE']
    # except KeyError as e:
    #     gnomad_max_maf_source = 'NA'
    # finally:
    #     print(record.CHROM, record.POS, gnomad_max_maf_source)
    new_row = pd.DataFrame([new_row_dict.values()], columns=new_row_dict.keys())
    rows.append(new_row)

    if dvd_count % 10000 == 0:
        print(dvd_count)
    # if record_of_interest is not None:
    #     break

with open('extracted_rows.pickle', 'wb') as f:
    pickle.dump(rows, f)


df = pd.concat(rows)

# output_df = pd.concat(rows)
# output_df.shape



df.to_csv('all_fields.csv')


for k,v in record_of_interest.INFO.items():
    if isinstance(v, list):
        print(k, type(v), v, len(v))
        if len(v) > 1:
            print('*'*30)
    else:
        print(k, type(v), v)


import pandas as pd
df = pd.read_csv('process_dvd_12-06-2023_only_MT-Chrom-2.csv', index_col=0)




reader = vcfpy.Reader.from_path(dvd_bgz)
dvd_count = 0
non_snv_count = 0
for record in reader:
    dvd_count += 1
    if not record.is_snv():
        non_snv_count += 1

    if dvd_count % 10000 == 0:
        print(dvd_count)
print("Total DVD Count:", dvd_count)
print("Non-SNP Count:", non_snv_count)
print("SNP Count:", dvd_count - non_snv_count)


# from typing import List
# def count_column_occurences(dfs: List[pd.DataFrame]):
#     seen_cols = {}
#     for df in dfs:
#         cols = df.columns.tolist()
#         for c in cols:
#             if c in seen_cols:
#                 seen_cols[c] += 1
#             else:
#                 seen_cols[c] = 0
#     return seen_cols


# with open(os.path.join(os.getcwd(), 'extracted_rows.pickle'), 'rb') as f:
#     picked_rows = pickle.load(f)