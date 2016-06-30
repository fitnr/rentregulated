BRONX = 10451 10452 10453 10454 10455 10456 10457 10458 10459 10460 10461 \
	10462 10463 10464 10465 10466 10467 10468 10469 10470 10471 10472 10473 \
	10474 10475

KINGS = 11200 11201 11203 11204 11205 11206 11207 11208 11209 11210 11211 \
	11212 11213 11214 11215 11216 11217 11218 11219 11220 11221 11222 11223 \
	11224 11225 11226 11228 11229 11230 11231 11232 11233 11234 11235 11236 \
	11237 11238 11239 11241 11242 11243 11249 11252

QUEENS = 11004 11100 11101 11102 11103 11104 11105 11106 11300 11354 11355 \
	11356 11357 11358 11359 11360 11361 11362 11363 11364 11365 11366 11367 \
	11368 11369 11370 11371 11372 11373 11374 11375 11377 11378 11379 11385 \
	11400 11411 11412 11413 11414 11415 11416 11417 11418 11419 11420 11421 \
	11422 11423 11424 11426 11427 11428 11429 11430 11432 11433 11434 11435 \
	11436 11600 11691 11692 11693 11694 11697

NEWYORK = 10000 10001 10002 10003 10004 10005 10006 10007 10009 10010 \
	10011 10012 10013 10014 10015 10016 10017 10018 10019 10020 10021 10022 \
	10023 10024 10025 10026 10027 10028 10029 10030 10031 10032 10033 10034 \
	10035 10036 10037 10038 10039 10040 10044 10045 10046 10048 10055 10060 \
	10065 10069 10075 10090 10098 10100 10103 10104 10105 10106 10107 10110 \
	10112 10115 10118 10119 10120 10121 10122 10123 10128 10151 10152 10153 \
	10154 10155 10162 10165 10166 10167 10169 10170 10173 10174 10176 10178 \
	10279 10280 10282 10400

RICHMOND = 10301 10302 10303 10304 10305 10306 10307 10308 10309 10310 \
	10312 10314

NASSAU = 11001 11003 11010 11020 11021 11023 11024 11030 11040 11042 \
	11050 11501 11507 11510 11514 11516 11518 11520 11530 11542 11545 \
	11548 11550 11552 11553 11554 11557 11559 11560 11561 11563 11565 \
	11566 11570 11572 11575 11576 11577 11580 11581 11590 11596 11598 \
	11696 11709 11710 11714 11732 11735 11753 11756 11758 11771 11783 \
	11791 11793 11801 11803 11804

ROCKLAND = 10901 10920 10923 10952 10956 10960 10965 10968 10970 10974 \
	10976 10977 10980 10983 10989

WESTCHESTER = 10501 10502 10505 10507 10520 10522 10523 10528 10530 10533 10538 \
	10543 10546 10547 10548 10549 10550 10552 10553 10562 10566 10570 10573 10578 \
	10580 10583 10588 10591 10598 10600 10601 10603 10604 10605 10606 10607 10610 \
	10700 10701 10703 10704 10705 10706 10707 10708 10709 10710 10801 10803 10804 \
	10805

ALBANY = 12054 12200 12202 12204 12205 12206 12207 12208 12209 12210 12211 12223 12226 12227

ERIE = 14201 14206 14209 14211 14213 14214 14215 14216 14217 14220 14222 14225

# These counties appear on the database search page, but a manual search shows 0 properties
# DUTCHESS = 12601
# MONROE = 14445
# RENSSELAER = 12180
# SCHENECTADY = 12305
# SUFFOLK = 17727

COUNTIES = BRONX KINGS QUEENS NEWYORK RICHMOND \
	NASSAU ROCKLAND WESTCHESTER ALBANY ERIE
	# DUTCHESS MONROE RENSSELAER SCHENECTADY SUFFOLK

csv = $(addsuffix .csv,$(COUNTIES))
zipcodefiles = $(foreach b,$(COUNTIES),$(foreach z,$($b),$b/$z.csv))

rentregulatedbuildings.csv: $(csv)
	echo buildingregistrationnumber,lastregistrationyear,address,zipcode,county,status,addtionaladdresses > $@
	cat $^ >> $@

.SECONDEXPANSION:
$(csv): %.csv: $$(foreach z,$$($$*),$$*/$$z.csv)
	grep --no-filename -v 'Displaying buildings' $^ | \
		sed 's/\[Additional Addresses\]/1/g' > $@

$(zipcodefiles): %.csv: | $$(@D)
	python3.5 scrape.py $(subst -, ,$(*D)) $(*F) > $@

counts.csv:
	echo county,zipcode,count > $@
	for f in $(basename $(zipcodefiles)); do \
		python3.5 scrape.py --action count $${f/\// } >> $@; \
	done;

$(COUNTIES):; mkdir -p $@
