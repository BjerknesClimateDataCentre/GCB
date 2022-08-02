def read_SOCAT(filepath, ddtype={0: str, 2: str}):
    import pandas as pd

    SOCATmetacolheadertextshort = 'Expocode\tversion\tDataset'
    SOCATcolheadertextshort = 'Expocode\tversion\tSource_DOI\tQC_Flag'

    separator = '\t'
    line = ''
    start_data_line = -1
    metaline = ''
    start_metadata_line = -1
    f = open(filepath)

    while SOCATmetacolheadertextshort not in metaline:
        metaline = f.readline()
        start_metadata_line = start_metadata_line + 1  # Where metadata lines start

    end_metadata_line = start_metadata_line
    while '\t' in metaline:
        metaline = f.readline()
        end_metadata_line = end_metadata_line + 1  # End of metadata lines

    # Create metadata dataframe
    SOCAT_metadata = pd.read_csv(filepath, sep='\t',
                                 skiprows=start_metadata_line,
                                 nrows=end_metadata_line - start_metadata_line - 1,
                                 dtype=ddtype)

    # Find where data columns start
    start_data_line = start_data_line + end_metadata_line
    while SOCATcolheadertextshort not in line:
        line = f.readline()
        start_data_line = start_data_line + 1
    f.close()

    # Read SOCAT data in dataframe
    #ddtype = {0: str, 2: str}  # add type str to columns 0 and 2
    # Read the SOCAT file into a pandas dataframe
    SOCAT_data = pd.read_csv(filepath, sep=separator, skiprows=start_data_line,
                             na_values='NaN', on_bad_lines='skip', dtype=ddtype)

    return SOCAT_data, SOCAT_metadata, start_metadata_line, end_metadata_line, start_data_line