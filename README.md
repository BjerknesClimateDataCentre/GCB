# GCB

Creates an overview of SOCAT measurements made in the previous year to be used for reporting to the Global Carbon Budget.

A tsv file containing:
<Platform    Start Datetime  End Datetime    Region  No. of samples (in XXXX)    Principal Investigator  DOI (if available)  QC flag Platform type   Days    Expocode>

The majority of information is fetched from the SOCAT synthesis global file. The region(s) are fetched from regional files, 
platform type is fetched from a separate file assembled from previous years GCB reports and added to as needed.

The SOCAT synthesis files are fetched from https://www.socat.info/index.php/data-access/
Last accessed 2020.07.06

Requires:
Global and regional synthesis SOCAT files
A previous version of the GCB for platform-type retrieval

Order of operations:
- Regions.py and platform_type.py must be run prior to this script.
 * Regions.py takes a long time to run. An hour+. Plan accordingly.

- When regions.csv and platform_type.csv is created this script can be run.

- The platform type is set to 'None' for all new/unknown platforms. 
  Go through GCB.csv and identify all new platforms (where platform-type is missing), 
  add them to the platform_type.csv with prefix, name and type, and run this main script again.

- Check the final GCB.csv and identify if any work needs to be done with regards to the DOIs. 
  Remove 'None'-entries if that is preferred. 


Maren Kjos Karlsen 2020-07-08
