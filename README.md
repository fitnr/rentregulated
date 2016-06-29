New York Rent Regulated Buildings 
---------------------------------

In New York, many privately-owned apartments are subject to limits on the rent landlords can ask. The vast majority of these apartments are called *rent-stabilized*. An older program, *rent-control*, has even stronger limits on rent increases and evictions.

Owners of buildings with rent-controlled and rent-stabilized apartments must register them with the state [Division of Housing and Community Renewal](http://www.nyshcr.org). The registry DHCR keeps also includes information about housing subsidy programs that apply to these buildings.

You can [search the DHCR registry](https://apps.hcr.ny.gov/BuildingSearch/), but it's difficult to get complete data. This data set was compiled using a computer program to methodically request all of data from the DCHR site in mid-2016.

The vast majority of properties are in the five boroughs, most of the rest are also downstate.

## Caveats
* DCHR has provided [basic information](https://apps.hcr.ny.gov/buildingsearch/popup.aspx) about the fields in the data set, but details about their methodology are missing.
* Some addresses are given as ranges ("6 TO 10 MAIN STREET").
* Some properties have "additional addressses". The significance of these addresses is unexplained. This data is available on the DHCR site, but requires an additional step to scrape, so only the note that an additional address exists is included.
* The `status` field includes a a space-separated of program or description that applies to a building. One or more status may be present. The exact wording of each status may differ slightly, so be careful with filtering. The statuses, with links to the best explanation available:
    * [MULTIPLE DWELLING A](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#DwellingA)
    * [MULTIPLE DWELLING B](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#DwellingB)
    * [HOTEL](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#Hotel)
    * [SINGLE ROOM OCCUPANCY](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#SingleRoom)
    * [GARDEN APARTMENT COMPLEX](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#Garden)
    * [NON-EVICT COOP/CONDO](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#NonEvict) (may include an effective date in parentheses)
    * [EVICT COOP/CONDO](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#Evict) (may include an effective date in parentheses)
    * [COOP/CONDO PLAN FILED](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#Coop) (may include a file date in parentheses)
    * [J-51](http://www1.nyc.gov/site/hpd/developers/tax-incentives-j51.page)
    * [421-A](http://www1.nyc.gov/site/hpd/developers/tax-incentives-421a.page)
    * [ARTICLE 11 OF PHFL](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#Article11)
    * [ARTICLES 14 & 15 OF PHFL](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#Article14and15)
    * Section 608
    * [Not Indicated by Owner](https://apps.hcr.ny.gov/buildingsearch/popup.aspx#NotIndicated)
    * RENT CONTROLLED APTS MAY EXIST
