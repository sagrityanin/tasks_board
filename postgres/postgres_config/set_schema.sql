CREATE SCHEMA tasks;
grant usage on schema tasks to SESSION_USER;
grant create on schema tasks to SESSION_USER;
ALTER ROLE SESSION_USER SET search_path = public, tasks;
grant SELECT, INSERT, UPDATE, DELETE on ALL tables in schema tasks TO SESSION_USER;
CREATE USER postgres SUPERUSER;
CREATE DATABASE postgres WITH OWNER postgres;

