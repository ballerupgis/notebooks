# Vejledning 
Vejledning i hentning af lokalplan-pdf til PostgreSQL
## 1. Klargør tabeller i databasen

Hent alle lokalplaner fra plansystems-WFS til PostgreSQL database:

```bash
ogr2ogr -f PostgreSQL PG:"dbname=xx host=xx port=xx user=xx password=xx" WFS:"http://geoservice.plansystem.dk/wfs?version=1.0.0" pdk:lokalplan -lco SCHEMA=proj_lokalplan_dokument -lco GEOMETRY_NAME=the_geom -nln "lokalplan" -a_srs "EPSG:25832"
```

Lav tabel i databasen til at indsætte planid, status og tilhørende dokumenttekst
```sql
# Lav skema og tabel
create schema proj_lokalplan_dokument;

create table proj_lokalplan_dokument.lokalplan_dokument (
	gid serial primary key not null,
	planid int4,
	plantype varchar,
	document text
)

## indsæt plandata ind i lokalplan_dokument
insert into proj_lokalplan_dokument.lokalplan_dokument(PLANID, PLANSTATUS)
SELECT PLANID, STATUS
FROM proj_lokalplan_dokument.lokalplan
where STATUS in ('V', 'F') and AKTUEL = TRUE
```

## 2. Hent plandoukmenter
Kør Python-script til at opdatere  

## 3. Opdateringer
Lokalplaner kan have følgende statuser - kladde, forslag, vedtage og aflyst. Vi er kun interesseret at oprette, opdatere eller fjerne lokalplandokumenter i ElasticSearch indexet når der sker ændring i planstatus. Ligeledes skal de data der trækkes fra WFS tilrettes i PostgreSQL. Opdateringsfrekvensen er selvfølgelig afgørende for om en plan kan springe en status over og som udgangspunkt kan opdateringen sættes til at ske en gang om måneden. Følgende scenarier gør sig gældende: 
#### Oprettes
* Planer der ændre status fra kladde til forslag
* Planer med planid som ikke allrede eksisterer (springer status over pga. opdateringfrekvensen)
#### Opdateres
* Planer der ændre status fra forslag til vedtaget
#### Slettes
* Planer der ændre status til aflyst

planid vil være det samme for en plan der ændre status, men i tabellen angives hvilken plan som er gældende i kolonnen aktuel.

