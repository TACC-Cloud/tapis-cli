'''Test for specific files existence in a directory'''
import pytest
import os

'''Parameterize the test with a list of required files'''
@pytest.mark.parametrize("file_list", [
    (['read1_fastqc.html', 'read1_fastqc.zip'])
])
def test_files(job_directory,file_list):
    '''checks job_directory for existence of all contents of file_list'''
    # Existence
    listdir = os.listdir(job_directory)
    assert(len(list(set(listdir) & set(file_list))) == len(file_list)), \
        "Missing files"
    # Files are readable and not zero length
    for f in file_list:
        try:
            fstat = os.stat(os.path.join(job_directory, f))
            assert (fstat.st_size > 0), "Zero length file: {}".format(f)
        except Exception:
            raise IOError("Couldn't stat {}".format(f))
