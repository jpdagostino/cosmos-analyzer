import os
import patoolib
from pathlib import Path

def get_extracted_path (path):
    extension = Path(path).suffixes[-1].strip('.')
    if extension in patoolib.ArchiveFormats or extension == "gz": # this is in the supported archive formats as .gzip
        extracted_path = path.strip(Path(path).suffixes[-1])
        if not os.path.exists(extracted_path):   
            patoolib.extract_archive(path)
            path = extracted_path # fits.gz -> fits
    return path