-- 1. How many countries speaks French
SELECT 
	COUNT(*) AS frech_speaking_countries
FROM 
	countries_info
WHERE 
	languages = 'French';

-- 2. How many countries speaks english
SELECT 
	COUNT(*) AS english_speaking_countries
FROM 
	countries_info
WHERE 
	languages = 'English';

-- 3. How many country have more than 1 official language
SELECT 
	COUNT(*) AS number_of_countries_with_multiple_languages
FROM 
	countries_info
WHERE 
	LENGTH(Languages) - LENGTH(REPLACE(Languages, ',', '')) > 0;

-- 4. How many country official currency is Euro
SELECT 
	COUNT(*) AS euro_countries
FROM 
	countries_info
WHERE 
	currency_name  = 'Euro';

-- 5. How many country is from West europe
SELECT 
	COUNT(*) AS west_europe_countries
FROM 
	countries_info
WHERE 
	sub_region  = 'Western Europe';

-- 6. How many country has not yet gain independence
SELECT 
	COUNT(*) AS no_independence
FROM 
	countries_info
WHERE 
	independence  = FALSE ;

-- 7. How many distinct continent and how many country from each
SELECT  
	DISTINCT COUNT(continents), continents AS total_countries
FROM 
	countries_info
GROUP BY 
	continents;

-- 8. How many country whose start of the week is not Monday
SELECT * 
FROM 
	countries_info
WHERE 
	startofweek != 'monday';

-- 9. How many countries are not a United Nation member
SELECT 
	COUNT(*) AS total_non_un_members
FROM 
	countries_info
WHERE 
	united_nation_members  = FALSE ;

-- 10. How many countries are United Nation member
SELECT 
	COUNT(*) AS total_un_members
FROM 
	countries_info
WHERE 
	united_nation_members  = TRUE ;

-- 11. Least 2 countries with the lowest population for each continents
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

-- 12. Top 2 countries with the largest Area for each continent
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

-- 13. Top 5 countries with the largest Area
SELECT * 
FROM 
	countries_info
ORDER BY area DESC
LIMIT 5;

-- 14. Top 5 countries with the lowest Area
SELECT * 
FROM 
	countries_info
ORDER BY area ASC
LIMIT 5;