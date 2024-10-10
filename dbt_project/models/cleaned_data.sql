-- models/cleaned_medical_businesses.sql

WITH raw_data AS (
    SELECT 
        message_id,
        date,
        text,
        sender_id
    FROM 
        {{ ref('telegram_data') }}
)
SELECT
    message_id,
    date,
    sender_id,
    CASE 
        WHEN text ILIKE '%pharmacy%' THEN 'Pharmacy'
        WHEN text ILIKE '%hospital%' THEN 'Hospital'
        ELSE 'Other'
    END AS business_type
FROM raw_data
WHERE text IS NOT NULL;
