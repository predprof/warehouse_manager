DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS stowages;

DROP SEQUENCE IF EXISTS items_seq;
CREATE SEQUENCE items_seq START WITH 100000;

DROP SEQUENCE IF EXISTS stowages_seq;
CREATE SEQUENCE stowages_seq START WITH 100000;

CREATE TABLE stowages
(
  id               INTEGER PRIMARY KEY DEFAULT nextval('stowages_seq'),
  name             VARCHAR(30)             NOT NULL,
  size_x           INTEGER                 NOT NULL,
  size_y           INTEGER                 NOT NULL,
  size_z           INTEGER                 NOT NULL,
  json	           VARCHAR(255)                NOT NULL,
  CONSTRAINT name_idx UNIQUE (name)
);

CREATE TABLE items
(
  id               INTEGER PRIMARY KEY DEFAULT nextval('items_seq'),
  name             VARCHAR(255)            NOT NULL,
  size_x           INTEGER                 NOT NULL,
  size_y           INTEGER                 NOT NULL,
  size_z           INTEGER                 NOT NULL,
  weight           INTEGER                 NOT NULL,
  status           VARCHAR(30)             NOT NULL,
  stowage_id       INTEGER                 ,
  FOREIGN KEY (stowage_id) REFERENCES stowages (id) ON UPDATE CASCADE
);

INSERT INTO items (name, size_x, size_y, size_z, weight, status) VALUES
('Системный блок 1', 900, 900, 300, 15, 'Не размещен'),
('Монитор', 900, 1500, 50, 7, 'Не размещен'),
('Доска маркерная', 1900, 1100, 900, 5, 'Не размещен');