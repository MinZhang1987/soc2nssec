* test_soc2nssec.do
* Checks soc2nssec against the ONS analytic-class tables (simplified method)
* for SOC90, SOC2000, SOC2010 and SOC2020.
* soc2nssec_test_ons.dta holds every unit group with the expected 7-class
* NS-SEC taken from the ONS derivation tables (analytic classes, "ssec" column;
* classes 1.1 and 1.2 combined into class 1).
* Run from the folder that holds soc2nssec.ado and the test data.

clear all
set more off
adopath ++ "`c(pwd)'"
discard

local versions "90 2000 2010 2020"
local nfail = 0

foreach v of local versions {

	use "soc2nssec_test_ons.dta", clear
	keep if socversion == `v'
	soc2nssec soc, gen(class7) version(`v')

	quietly count if class7 != expected7
	local nbad = r(N)
	di as text "SOC`v': " _N " unit groups, " as result `nbad' as text " mismatches"
	if `nbad' > 0 {
		list soc expected7 class7 if class7 != expected7, noobs sep(0)
		local nfail = `nfail' + `nbad'
	}
}

* Codes that are not SOC2020 unit groups should become missing
clear
input soc
1113
1111
5000
9269
.
end
soc2nssec soc, gen(class7) version(2020)
list, noobs
assert missing(class7) if inlist(soc, 1113, 5000, .)
assert class7 == 1 if soc == 1111
assert class7 == 7 if soc == 9269

* Out-of-range codes should stop with an error
clear
input soc
1111
12345
end
capture noisily soc2nssec soc, gen(class7) version(2020)
assert _rc == 459

* An unsupported version should stop with an error
capture noisily soc2nssec soc, gen(class7b) version(15)
assert _rc == 198

di as text _n "Total mismatches across versions: " as result `nfail'
assert `nfail' == 0
di as result "All tests passed."
