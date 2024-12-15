DELETE FROM auth WHERE is_active = True;
DELETE FROM "user" WHERE user_type = 'ind';
DELETE FROM "user" WHERE user_type = 'org';