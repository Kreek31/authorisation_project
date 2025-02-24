-- Таблица с информацией о ролях пользователей
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

COMMENT ON TABLE roles IS 'Информация о ролях пользователей';

COMMENT ON COLUMN roles.role_id IS 'Уникальный идентификатор роли';

COMMENT ON COLUMN roles.role_name IS 'Название роли';

-- Таблица для хранения информации о пользователях
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    chat_id UNIQUE BIGINT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash BYTEA NOT NULL,
    role_id INT REFERENCES roles(role_id) ON DELETE CASCADE
);

COMMENT ON TABLE users IS 'Информация о пользователях';

COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN users.password_hash IS 'Хэш пароля пользователя';

COMMENT ON COLUMN users.role_id IS 'идентификатор роли';

-- Таблица для хранения информации о пользователях, зарегестрированный через yandex
CREATE TABLE yandex_users (
	user_id SERIAL PRIMARY KEY,
    chat_id UNIQUE BIGINT,
	username VARCHAR(50) NOT NULL,
	role_id INT REFERENCES roles(role_id) ON DELETE CASCADE
);

COMMENT ON TABLE yandex_users IS 'Информация о пользователях, зарегестрированных через яндекс';

COMMENT ON COLUMN yandex_users.user_id IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN yandex_users.username IS 'Никнейм пользователя';

COMMENT ON COLUMN yandex_users.role_id IS 'идентификатор роли';

-- Таблица с историей заходов
CREATE TABLE login_logs(
	log_id SERIAL PRIMARY KEY,
	user_id BIGINT,
	login_type VARCHAR(32),
	date TIMESTAMP
);

COMMENT ON TABLE login_logs IS 'Логи заходов';

COMMENT ON COLUMN login_logs.log_id IS 'Уникальный идентификатор лога';

COMMENT ON COLUMN login_logs.user_id IS 'Идентификатор пользователя';

COMMENT ON COLUMN login_logs.login_type IS 'Как пользователь авторизовался (через наш сервис, yandex и т. п.)';

COMMENT ON COLUMN login_logs.date IS 'Дата создания лога';

-- Процедура логирования заходов
CREATE OR REPLACE PROCEDURE login_logs_add(
    p_user_id BIGINT,
    p_login_type VARCHAR(32)
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO login_logs (user_id, login_type, date)
    VALUES (p_user_id, p_login_type, current_timestamp);
END;
$$;