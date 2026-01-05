# TODO By Release


## R4 Load subcategories and descriptions

Goal: Load subcategories and descriptions to zoom into expendings analysis.

- [x] add subcategory and desc on data_model.ing.movimientos_csv
- [x] update extract to use subcategory and desc
- [x] add idem on db.ing.movimientos_staging
- [x] update table movimientos_staging
- [x] update mview movimientos_mview with subcategory and desc
- [ ] execute ETL main to backfill movementos from 2023, 2024 and 2025
- [ ] refresh movimientos_mview
- [ ] update notebook with cat analysis

## R3 Analylitical Zoom on Categories

Goal: Zoom in to check the amount of money spent by cat and the trend.

- [x] add category on data_model.ing.movimientos_csv
- [x] update extract to use cat
- [x] add idem on db.ing.movimientos_staging
- [x] update database
- [x] update movimientos_mview with cat
- [x] execute ETL main
- [x] refresh movimientos_mview
- [x] update notebook with cat analysis

