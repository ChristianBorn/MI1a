-- SRC: http://goblor.de/wp/2009/10/17/openstreetmap-projekt-teil2-%e2%80%93-von-den-rohdaten-zum-gerichteten-graphen/
CREATE TABLE `verbindungen` (
  `wayid` bigint(20) NOT NULL,
  `start` bigint(20) NOT NULL,
  `end` bigint(20) NOT NULL,
  `distance` double NOT NULL default '0',
  KEY `start` (`start`),
  KEY `end` (`end`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
