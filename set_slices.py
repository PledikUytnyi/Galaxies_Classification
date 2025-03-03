import pandas as pd
import ast

slice_max_number=100
all_data_train = pd.DataFrame(columns=['flux', 'spiral', 'elliptical', 'uncertain','lambda_rest'])
all_data_train.to_csv('all_data.csv', index=None, sep=' ', mode='w')

def to_list(row):
    return ast.literal_eval(row)


class data_slice:
    def __init__(self, file):
        self.lambdas = file['lambdas'].apply(to_list)
        self.flux = file['flux'].apply(to_list)
        self.factor_lambda = 1 / (1 + file['z'])
        self.label_spiral = file['SPIRAL']
        self.label_elliptical = file['ELLIPTICAL']
        self.label_uncertain = file['UNCERTAIN']
        self.lambda_rest = pd.Series(
            [[num * scalar for num in lst] for lst, scalar in zip(self.lambdas, self.factor_lambda)])
    @staticmethod
    def create(file_path):
        file = pd.read_csv(file_path, header=0, delimiter=' ')
        return data_slice(file)


with open("healpx_to_download.txt", "r") as file:
    lines = file.readlines()

to_download = [line.strip() for line in lines]

for i in to_download[:slice_max_number]:
    obj_slice = data_slice.create(f"final_merged_data/healpx{i}.txt")
    pd_slice = pd.DataFrame(
        {'flux': obj_slice.flux, 'spiral': obj_slice.label_spiral, 'elliptical': obj_slice.label_elliptical,
         'uncertain': obj_slice.label_uncertain})
    pd_slice['lambda_rest'] = obj_slice.lambda_rest
    pd_slice.to_csv('all_data.csv', index=None, sep=' ', mode='a', header=False)

