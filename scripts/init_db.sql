CREATE DATABASE publications_db;
CREATE USER pub_user WITH PASSWORD 'pub_pass';
ALTER DATABASE publications_db OWNER TO pub_user;
