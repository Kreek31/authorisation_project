-- Вставка ролей в таблицу roles
INSERT INTO
    roles (role_name, role_id)
VALUES
    ('Администратор', 1),
    ('Пользователь', 2);


-- Вставка пользователей в таблицу users
INSERT INTO
    users (user_id, username, password_hash, role_id)
VALUES
    (1, 'admin1', '$2b$12$kwkvyX0b20aKmAt/nSJ7EOsCLsIVZoitzq4Rj6tmGSHmJPYLzY09u', 1), --123
    (2, 'user1', '$2b$12$5p5ybk9OBiqJqxs2.s38ZefUGADh5A2FTMbeuaKbzn50f6IL/cBlm', 2); --456