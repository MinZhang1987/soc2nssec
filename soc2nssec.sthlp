{smcl}

{title:Title}
{bf:soc2nssec}{hline 2}creates seven-level NSSEC class from SOC}

{title:Syntax}
{p}
soc2nssec {it:varname} [if] [in] , GENerate({it:newvar}) Version({it:90 00 10}) noLabel
{p_end}


{title:Description}
{p}
{bf:soc2nssec} converts Standard Occupational Classification to the National Statistics Socio-economic Classification class (seven-level NSSEC). It supports SOC1990, SOC2000, and SOC2010. It also provides value labels for seven-level NSSEC class.
{p_end}


{title:Remark}
{p}
{bf:soc2nssec} uses simplified methods to derive seven-level NSSEC analytic class based on the following documents: 
The National Statistics Socio-economic Classification: (Rebased on the SOC2010) User Manual; The National Statistics Socio-economic Classification: Origins, Development and Use (for SOC90 and SOC2000). 
{p_end}

{p}
{bf:soc2nssec} supports only 3-digit SOC90, 4-digit SOC00, and 4-digit SOC10.
{p_end}

{p}
{bf:soc2nseec} creates value labels for the derived NSSEC class variable. Value labels are named as newvar_nssec7. Users can use the command "label, modify" to change the labels. 
{p_end}

{title:Option}
{p}
{bf:generate(newvar)} creates a new variable for seven-level NSSEC class.
{p_end}
{p}
{bf:version(90 00 10)} indicates the version of SOC that is used. 
{p_end}
{p}
{bf:noLabel} indicates that no value label would be created. 
{p_end}

{title:Examples:}
{p}
soc2nssec jobsoc00, gen(class7) v(00)
{p_end}

{title:Author:}
{p}
Min Zhang, University of Manchester, UK. Email: zhangmin.ac@gmail.com
{p_end}
