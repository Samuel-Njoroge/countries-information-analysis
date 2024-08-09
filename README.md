# Countries Information Analysis
A simple analysis on countries in different parts of the world. The objective of this project is to provide first hand information to aid in planning such as international visits and relocation. 

## Architecture
![countries_information](https://github.com/user-attachments/assets/ed9b01c0-4f97-41f6-8df4-4a62459cee70)

## Skills 
- API - Extracting data from an API `RestCountries`
- SQL - Data manipulation with SQL.
 > Aggregate Functions
  > 
  > Window Functions
  > 
  > Common Table Expressions (CTEs)
- Python & Pandas - Data cleaning and transformation.

## Steps Taken
1. Extracting data from the [Rest Countries API](https://restcountries.com/v3.1/all)
2. Data cleaning and transformation.
3. Loading the data into PostgreSQL in the table `countries_info` and further analysis using SQL. 
4. Data Visualization using Tableau.
   
## Objectives
### 1. How many countries speaks French?
#### Query
```sh
SELECT 
	COUNT(*) AS frech_speaking_countries
FROM 
	countries_info
WHERE 
	languages = 'French';
```

### 2. How many countries speaks english?
#### Query
```sh
SELECT 
	COUNT(*) AS english_speaking_countries
FROM 
	countries_info
WHERE 
	languages = 'English';
```

### 3. How many countries have more than 1 official language?
#### Query
```sh
SELECT 
	COUNT(*) AS number_of_countries_with_multiple_languages
FROM 
	countries_info
WHERE 
	LENGTH(Languages) - LENGTH(REPLACE(Languages, ',', '')) > 0;
```

### 4. How many countries use Euro as the official currency?
#### Query
```sh
SELECT 
	COUNT(*) AS euro_countries
FROM 
	countries_info
WHERE 
	currency_name  = 'Euro';
```

### 5. How many countries are from West europe?
#### Query
```sh
SELECT 
	COUNT(*) AS west_europe_countries
FROM 
	countries_info
WHERE 
	sub_region  = 'Western Europe';
```

### 6. How many countries have not yet gained independence?
#### Query
```sh
SELECT 
	COUNT(*) AS no_independence
FROM 
	countries_info
WHERE 
	independence  = FALSE ;
```

### 7. How many distinct continents and how many countries from each?
#### Query
```sh
SELECT  
	DISTINCT COUNT(continents), continents AS total_countries
FROM 
	countries_info
GROUP BY 
	continents;
```

### 8. How many countries whose start of the week is not Monday?
#### Query
```sh
SELECT * 
FROM 
	countries_info
WHERE 
	startofweek != 'monday';
```

### 9. How many countries are not United Nation members?
#### Query
```sh
SELECT 
	COUNT(*) AS total_non_un_members
FROM 
	countries_info
WHERE 
	united_nation_members  = FALSE ;
```

### 10. How many countries are United Nation members?
#### Query
```sh
SELECT 
	COUNT(*) AS total_un_members
FROM 
	countries_info
WHERE 
	united_nation_members  = TRUE ;
```

### 11. Least 2 countries with the lowest population for each continents
#### Query
```sh
WITH RankedCountries AS (
	SELECT
		country_name,
		continents,
		population,
		ROW_NUMBER() OVER (PARTITION BY continents ORDER BY population ASC) AS RANK 
	FROM countries_info
)
SELECT
	country_name,
	continents,
	population
FROM RankedCountries
WHERE rank <= 2;
```

### 12. Top 2 countries with the largest Area for each continent
#### Query
```sh
WITH LargestArea AS (
	SELECT 
		country_name,
		continents,
		area,
		ROW_NUMBER() OVER (PARTITION BY continents ORDER BY area DESC) AS rank
	FROM countries_info
)
SELECT
	country_name,
	continents,
	area 
FROM LargestArea
WHERE RANK <=2;
```

### 13. Top 5 countries with the largest Area
#### Query
```sh
SELECT * 
FROM 
	countries_info
ORDER BY area DESC
LIMIT 5;
```

### 14. Top 5 countries with the lowest Area
#### Query
```sh
SELECT * 
FROM 
	countries_info
ORDER BY area ASC
LIMIT 5;
```
