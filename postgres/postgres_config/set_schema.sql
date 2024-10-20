CREATE SCHEMA task;
grant usage on schema task to SESSION_USER;
grant create on schema task to SESSION_USER;
ALTER ROLE SESSION_USER SET search_path = public, task;
grant SELECT, INSERT, UPDATE, DELETE on ALL tables in schema task TO SESSION_USER;
-- CREATE USER postgres SUPERUSER;
-- CREATE DATABASE postgres WITH OWNER postgres;
INSERT INTO status_title (title) VALUES ('Создана'), ('Выполнена'), ('Отклонена');

