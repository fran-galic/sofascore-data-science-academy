SELECT COUNT(DISTINCT user_pseudo_id) AS num_buzzer_feed_users
FROM bq.events
WHERE event_name = 'drawer_action' AND item_name= 'Buzzer Feed'
