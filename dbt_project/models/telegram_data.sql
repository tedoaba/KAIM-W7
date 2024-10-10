-- models/telegram_data.sql

SELECT 
    message_id,
    date,
    text,
    sender_id
FROM 
    telegram_medical_businesses;
