# soc2nssec
soc2nssec derives seven-level NSSEC (The National Statistics Socio-economic Classification) analytic class from Standard Occupational Classifications: SOC90, SOC2000, and SOC2010. 

Using the simplified method, soc2nssec follows the instruction of the official documents, "The National Statistics Socio-economic Classification User Manual" (for SOC90 and SOC2000) and "Volume 3 The National Statistics Socio-economic Classification: (Rebased on the SOC2010) User Manual".

Please note that soc2nssec uses the simplified method to derive the NSSEC class. It requires the complete information of SOC unit group (i.e., 3-digit SOC90, 4-digit SOC2000, or 4-digit SOC2010). 


# Example
use soc2nssec_sample_data

soc2nssec jobsoc00, gen(class7) version(00)

* where the variable jobsoc00 refers to SOC2000, which exists in the sample data; the variable class7 is newly generated NSSEC 7-level class; version(00) claims SOC2000. 

* It creates value labels according to seven-level NSSEC scheme. To switch it off, add the option "nolabel".

* Stata help file is included. Type "help soc2nssec" in Stata to view the help file.

# How to install a personal ado file
* Download the ZIP file.

* Extract the contents of the ZIP file to a temporary folder.

* Type "personal" in Stata and note the location of your personal ado-directory (for Windows users, usually c:\ado\personal\ ).

* Copy and paste the ado-directory in the window folder. Very likely that the folder is hidden.

* Move all extracted files to the personal ado-directory.

* Please note that the sample data are not built in Stata. Users need to save the sample data somewhere else and open it as the personal data.
 

# Author:
Min Zhang, The University of Manchester

Any feedback or questions, please contact zhangmin.ac@gmail.com

