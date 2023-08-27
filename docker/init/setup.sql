-- must change your name and databasename, passward.
CREATE ROLE task_app_admin LOGIN PASSWORD 'postgres';
CREATE DATABASE task_app_admin;
CREATE DATABASE task_app_test;
GRANT ALL PRIVILEGES ON DATABASE task_app_admin TO task_app_admin;
GRANT ALL PRIVILEGES ON DATABASE task_app_test TO task_app_admin;
ALTER ROLE task_app_admin WITH CREATEROLE CREATEDB SUPERUSER;
