DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS stowages;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP SEQUENCE IF EXISTS stowage_seq;
CREATE SEQUENCE stowage_seq START WITH 100000;

CREATE TABLE stowages
(
  id               INTEGER PRIMARY KEY DEFAULT nextval('stowage_seq'),
  row              VARCHAR(30)             NOT NULL,
  level            INTEGER                 NOT NULL,
  size_x           INTEGER                 NOT NULL,
  size_y           INTEGER                 NOT NULL,
  size_z           INTEGER                 NOT NULL,
  volume           bigint                  NOT NULL,
  json	           VARCHAR(255)            NOT NULL,
  empty            BOOLEAN                 NOT NULL,
  CONSTRAINT row_level_idx UNIQUE (row, level)
);

CREATE TABLE items
(
  id               uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  name             VARCHAR(255)            NOT NULL,
  size_x           INTEGER                 NOT NULL,
  size_y           INTEGER                 NOT NULL,
  size_z           INTEGER                 NOT NULL,
  weight           INTEGER                 NOT NULL,
  stowage_id       INTEGER                 ,
  FOREIGN KEY (stowage_id) REFERENCES stowages (id) ON UPDATE CASCADE
);

INSERT INTO items (name, size_x, size_y, size_z, weight) VALUES
('Системный блок 1', 900, 900, 300, 15),
('Монитор', 900, 1500, 50, 7),
('Доска маркерная', 1900, 1100, 900, 5);