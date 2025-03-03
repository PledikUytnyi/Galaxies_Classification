import pandas as pd
import numpy
import healpy
import h5py

n_side = 16
ra_df_orig = pd.DataFrame()
data_final = pd.DataFrame()
train_list = pd.read_csv('GalaxyZoo1_DR_table2.csv')
count = 500
RA_HOURS = 'RAhours'
RA_MINUTES = 'RAminutes'
RA_SECONDS = 'RAseconds'

DEC_DEGREES = 'DECdegrees'
DEC_MINUTES = 'DECminutes'
DEC_SECONDS = 'DECseconds'


def extract_degrees_hours(time_str):
    degrees_part = time_str.split(':')[0]
    return int(degrees_part)


def extract_minutes(time_str):
    minutes_part = time_str.split(':')[1]
    return int(minutes_part)


def extract_seconds(time_str):
    seconds_part = time_str.split(':')[-1]
    return float(seconds_part)


def convert_to_healpx(row):
    return healpy.ang2pix(n_side, row['theta'], row['phi'], nest=True, lonlat=False)


def floor_radec(row):
    return numpy.floor(row * 10 ** 4)


def merge_healpx(healpx):
    # sorting and merge values
    file_path = f"spectrum_data/data/MultimodalUniverse/v1/sdss/sdss/healpix={healpx}/001-of-001.hdf5"
    h5py_file = h5py.File(file_path)

    # our original data with labels
    data_orig = filtered_healpx[filtered_healpx['healpx'] == healpx].copy()
    data_orig['theta'] = data_orig['theta'].apply(floor_radec)
    data_orig['phi'] = data_orig['phi'].apply(floor_radec)

    # do the same for the downloaded data from sdss
    ra_df_orig['phi'] = pd.DataFrame(numpy.array(h5py_file['ra'])).apply(floor_radec)
    ra_df_orig['theta'] = (90 - pd.DataFrame(numpy.array(h5py_file['dec']))).apply(floor_radec)

    # add list of wavelengths to the data
    lambdas = numpy.array(h5py_file['spectrum_lambda'])
    ra_df_orig['lambdas'] = pd.DataFrame({'lambdas': lambdas.tolist()})
    # red shift value
    ra_df_orig['z'] = pd.DataFrame(numpy.array(h5py_file['Z']))
    # flux
    fluxes = numpy.array(h5py_file['spectrum_flux'])
    ra_df_orig['flux'] = pd.DataFrame({'flux': fluxes.tolist()})

    # merging two data sets
    rad_df_healpx_merge = ra_df_orig.merge(data_orig, on=['theta', 'phi'], how='inner')

    return rad_df_healpx_merge


train_list[RA_HOURS] = train_list['RA'].apply(extract_degrees_hours)
train_list[RA_MINUTES] = train_list['RA'].apply(extract_minutes)
train_list[RA_SECONDS] = train_list['RA'].apply(extract_seconds)

train_list[DEC_DEGREES] = train_list['DEC'].apply(extract_degrees_hours)
train_list[DEC_MINUTES] = train_list['DEC'].apply(extract_minutes)
train_list[DEC_SECONDS] = train_list['DEC'].apply(extract_seconds)
# phi and theta in radians
train_list['phi'] = 15 * (train_list[RA_HOURS] + train_list[RA_MINUTES] / 60 + train_list[RA_SECONDS] / 3600) * (
        numpy.pi / 180)
train_list['theta'] = (90 - (
        train_list[DEC_DEGREES] + train_list[DEC_MINUTES] / 60 + train_list[DEC_SECONDS] / 3600)) * (numpy.pi / 180)
train_list['healpx'] = train_list.apply(convert_to_healpx, axis=1)

# converting to degrees

train_list['phi'] = train_list['phi'] * (180 / numpy.pi)
train_list['theta'] = train_list['theta'] * (180 / numpy.pi)

# finding matching data
healpx_original = pd.read_csv('sdss_healpix.txt', header=0)
filtered_healpx = train_list[train_list['healpx'].isin(healpx_original['healpx'])]

# selecting healpx where the number of rows is larger than 'count' to avoid downloading too much data

healpx_value_counts = filtered_healpx['healpx'].value_counts().reset_index()
healpx_value_counts.columns = ['healpx', 'count']

# saving to file only those healpx indices that have large count
list_healpix = healpx_value_counts[healpx_value_counts['count'] > count]['healpx']
# saving the healpix list to a file
list_healpix.to_csv(r'healpx_to_download.txt', header=None, index=None, sep=' ', mode='w')

# composing our data: labels plus spectra

for healpx in list_healpix:
    result_merge = merge_healpx(healpx)
    # write data for each healpix to a separate file
    result_merge.to_csv(f'final_merged_data/healpx{healpx}.txt', index=None, sep=' ', mode='w')
