import subprocess

with open("healpx_to_download.txt", "r") as file:
    lines = file.readlines()

to_download = [line.strip() for line in lines]

# download some data using bash scripts
wget_path = '/opt/homebrew/bin/wget'


def download_healpix(h):
    bash_script = (
        f"{wget_path} -r -np -nH --cut-dirs=1 -R 'index.html*' -P ~/your_folder/spectrum_data "
        f"https://users.flatironinstitute.org/~polymathic/data/MultimodalUniverse/v1/sdss/sdss/healpix={h}/"
    )
    subprocess.run(bash_script, shell=True, capture_output=True, text=True)

    for healpx in to_download:
        download_healpix(healpx)
