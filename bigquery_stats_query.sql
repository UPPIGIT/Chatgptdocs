-- BigQuery stats with duration buckets
SELECT 
  CASE 
    WHEN DATE(creation_time) BETWEEN '2025-06-01' AND '2025-06-12' THEN 'June 1-12'
    WHEN DATE(creation_time) BETWEEN '2025-06-14' AND '2025-06-26' THEN 'June 14-26'
  END as period,
  
  COUNT(*) as total_jobs,
  ROUND(SUM(total_bytes_processed) / 1024 / 1024 / 1024, 2) as bytes_processed_gb,
  ROUND(SUM(total_bytes_billed) / 1024 / 1024 / 1024, 2) as bytes_billed_gb,
  
  -- Duration buckets (up to 15 seconds)
  SUM(CASE WHEN TIMESTAMP_DIFF(end_time, start_time, SECOND) <= 1 THEN 1 ELSE 0 END) as jobs_under_1sec,
  SUM(CASE WHEN TIMESTAMP_DIFF(end_time, start_time, SECOND) BETWEEN 1.01 AND 2 THEN 1 ELSE 0 END) as jobs_1_to_2sec,
  SUM(CASE WHEN TIMESTAMP_DIFF(end_time, start_time, SECOND) BETWEEN 2.01 AND 5 THEN 1 ELSE 0 END) as jobs_2_to_5sec,
  SUM(CASE WHEN TIMESTAMP_DIFF(end_time, start_time, SECOND) BETWEEN 5.01 AND 10 THEN 1 ELSE 0 END) as jobs_5_to_10sec,
  SUM(CASE WHEN TIMESTAMP_DIFF(end_time, start_time, SECOND) BETWEEN 10.01 AND 15 THEN 1 ELSE 0 END) as jobs_10_to_15sec,
  SUM(CASE WHEN TIMESTAMP_DIFF(end_time, start_time, SECOND) > 15 THEN 1 ELSE 0 END) as jobs_over_15sec,
  
  -- Average duration
  ROUND(AVG(TIMESTAMP_DIFF(end_time, start_time, SECOND)), 1) as avg_duration_sec,
  ROUND(MAX(TIMESTAMP_DIFF(end_time, start_time, SECOND)), 1) as max_duration_sec
  
FROM `your-project.region-us.INFORMATION_SCHEMA.JOBS`
WHERE 
  user_email = 'your-service-account@project.iam.gserviceaccount.com'
  AND start_time IS NOT NULL
  AND end_time IS NOT NULL
  AND (
    (DATE(creation_time) BETWEEN '2025-06-01' AND '2025-06-12')
    OR 
    (DATE(creation_time) BETWEEN '2025-06-14' AND '2025-06-26')
  )
GROUP BY period
ORDER BY period;