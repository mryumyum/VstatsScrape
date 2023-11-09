SELECT *
FROM dbo.Hololive_2022
WHERE Stream_Start_Time_UST IS NULL;


SELECT Video_ID, Creator, Stream_Start_Time_JST, Month_UST, SuperChat_total
FROM dbo.Hololive_2022
WHERE Creator = 'Yuzuki Choco';

SELECT Month,


-- Number One rankings
WITH rankings AS (  SELECT DENSE_RANK() OVER(PARTITION BY DATENAME(mm, publishedAt) ORDER BY SUM(SuperChat_total) DESC) AS month_rank, 
					DATENAME(mm, publishedAt) AS Month, 
					Creator, 
					ROUND(SUM(SuperChat_total), 2) As Tot_sc_22

					FROM dbo.Hololive_2022
					GROUP BY DATENAME(mm, publishedAt), Creator)
SELECT month_rank, Month, Creator, Tot_sc_22
FROM rankings
WHERE month_rank = 1
ORDER BY Tot_sc_22 DESC;


-- Number of Times at Number One
WITH rankings AS (  SELECT DENSE_RANK() OVER(PARTITION BY DATENAME(mm, publishedAt) ORDER BY SUM(SuperChat_total) DESC) AS month_rank, 
					DATENAME(mm, publishedAt) AS Month, 
					Creator, 
					ROUND(SUM(SuperChat_total), 2) As Tot_sc_22

					FROM dbo.Hololive_2022
					GROUP BY DATENAME(mm, publishedAt), Creator)
SELECT Creator, COUNT(*) times_at_no_1
FROM rankings
WHERE month_rank = 1
GROUP BY Creator
ORDER BY COUNT(*) DESC;


-- Total of how much each branch made and the ratio of that total to the number of streamers in each branch
SELECT Branch, 
		COUNT(DISTINCT(Creator)) AS Num_streamers_Branch, 
		ROUND(SUM(SuperChat_total), 2) AS Branch_Tot, 
		ROUND(SUM(SuperChat_total)/COUNT(DISTINCT(Creator)),2) AS SC_per_num_streamers
FROM dbo.Hololive_2022
GROUP BY Branch
ORDER BY Branch_Tot DESC;


SELECT DISTINCT(Creator)
FROM dbo.Hololive_2022;


-- Get month rankings
WITH rankings AS (  SELECT EOMONTH(Stream_Start_Time_UST) AS Month,
							Creator,
							Branch,
							COUNT(Creator) AS Times_Streamed_that_month,
							DAY(EOMONTH(Stream_Start_Time_UST)) AS DaysInMonth,
							DENSE_RANK() OVER(PARTITION BY DATENAME(mm, EOMONTH(Stream_Start_Time_UST)) ORDER BY SUM(SuperChat_total) DESC) AS SC_month_rank,
							DENSE_RANK() OVER(PARTITION BY DATENAME(mm, EOMONTH(Stream_Start_Time_UST)) ORDER BY AVG(Avg_viewers) DESC) AS AVG_viewers_month_rank,
							ROUND(SUM(SuperChat_total), 2) AS Tot_sc_for_month,
							ROUND(AVG(SuperChat_total), 2) AS AVG_Sc_Per_Stream,
							ROUND(AVG(NULLIF(SuperChat_total, 0)), 2) AS AVG_Sc_Per_Stream_ZERO_Ignored,
							ROUND(AVG(Avg_viewers), 2) AS AVG_viewers_month,
							ROUND(AVG(MAX_viewers), 2) AS AVG_MAX_viewers_month

							FROM dbo.Hololive_2022
							GROUP BY EOMONTH(Stream_Start_Time_UST), Creator, Branch)

SELECT DATENAME(mm, Month) AS Month_conv,
		Creator,
		Branch,
		Times_Streamed_that_month,
		ROUND(CAST(Times_Streamed_that_month AS FLOAT)/CAST(DaysInMonth AS FLOAT), 2) AS Stream_Freq,
		SC_month_rank,
		AVG_viewers_month_rank,
		Tot_sc_for_month,
		AVG_Sc_Per_Stream,
		AVG_Sc_Per_Stream_ZERO_Ignored,
		AVG_viewers_month,
		AVG_MAX_viewers_month
FROM rankings
--WHERE DATENAME(mm, Month) = 'April'
ORDER BY Month(Month), Tot_sc_for_month DESC;
--WHERE Creator = 'Usada Pekora'
--ORDER BY Tot_sc_for_month DESC;


SELECT Creator,
		Branch,
		COUNT(Creator) AS Times_Streamed_that_month,
		ROUND(SUM(SuperChat_total), 2) AS Tot_sc_for_month,
		ROUND(AVG(SuperChat_total), 2) AS AVG_Sc_Per_Stream,
		ROUND(AVG(NULLIF(SuperChat_total, 0)), 2) AS AVG_Sc_Per_Stream_ZERO_Ignored,
		ROUND(AVG(Avg_viewers), 2) AS AVG_viewers,
		ROUND(AVG(MAX_viewers), 2) AS AVG_MAX_viewers

FROM dbo.Hololive_2022
GROUP BY Creator
ORDER BY ROUND(SUM(SuperChat_total), 2)


SELECT Creator,
		SUM(SuperChat_total)
FROM dbo.Hololive_2022
GROUP BY Creator
ORDER BY SUM(SuperChat_total) DESC;

SELECT Creator, DATEADD(dd, 0, DATEDIFF(dd, 0, Stream_Start_Time_UST)), AVG_viewers
FROM dbo.Hololive_2022
WHERE Creator = 'Usada Pekora';

SELECT vt.URL, 
		vt.Video_ID, 
		vt.Video_Title, 
		vt.Creator, 
		hb.Branch, 
		vt.Avg_viewers, 
		vt.Max_viewers, 
		ROUND(vt.SuperChat_total, 2) AS Superchat_total, 
		vt.Stream_Start_Date_UST,  
		vt.Stream_Start_Time_UST, 
		vt.Duration
FROM dbo.vstats_2022 AS vt
JOIN dbo.Hololive_channel_info AS hb
ON vt.Creator = hb.Creator;