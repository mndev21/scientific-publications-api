CREATE DATABASE publications_db;
CREATE USER pub_user WITH PASSWORD 'pub_pass';
ALTER DATABASE publications_db OWNER TO pub_user;


CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX ix_pub_abstract_gin
ON publications USING gin ((abstract::text) gin_trgm_ops);
