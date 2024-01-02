from typing import Iterable
import vcfpy
import pandas as pd

import logging
import traceback

class VCFChromosome:
    def __init__(self, number):
        self.chromosome = number
        self.cols = set()
        self.records = []
        self.count = 0
        self.df = None
        self.bad_records = []
        self.bad_record_count = 0
    
    def add_records(self, record_list: Iterable[vcfpy.record.Record]):
        try:
            for record in record_list:
                self.add_record(record)
        except Exception as e:
            logging.error(traceback.format_exc())
            print(f"Occured at {self.count}")
            self.bad_records.append(record)
            self.bad_record_count += 1

    def add_record(self, record: vcfpy.record.Record):
        self.cols.update(record.INFO.keys())
        self.records.append(record)
        self.count += 1
        if self.count % 10000 == 0:
            print(self.count)
        # logging.error(traceback.format_exc())

    def _to_dataframe(self):
        record_list = []
        for record in self.records:
            info = record.INFO
            record_dict = {'CHROM': record.CHROM, 'REF': record.REF, 'ALT': record.ALT, 'POS': record.POS}
            for key, value in info.items():
                if isinstance(value, list):
                    if len(value) == 0:
                        pass
                    elif len(value) == 1:
                        value = str(value[0])
                    else:
                        value = ','.join(value)
                record_dict[key] = value
            record_list.append(record_dict)
        return pd.DataFrame.from_records(record_list)

            
    def _separate_variant_column(self):
        self.df['TYPE'] = self.df.TYPE.apply(lambda x:[0].type)
        self.df['ALT'] = self.df.TYPE.apply(lambda x:[0].value)

        cols = self.df.columns.tolist()
        new_col_order = cols[0:4] + [cols[-1], 'GENE'] + [c for c in cols[4:-1] if c != 'GENE']
        self.df = self.df[new_col_order]


    def update_dataframe(self):
        self.df = self._to_dataframe()
        self._separate_variant_column()