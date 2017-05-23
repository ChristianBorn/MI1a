-- SRC: http://goblor.de/wp/2009/10/17/openstreetmap-projekt-teil2-%e2%80%93-von-den-rohdaten-zum-gerichteten-graphen/
CREATE TABLE  `osm`.`verbindungen` (
  `wayid` int(11) NOT NULL,
  `start` int(11) NOT NULL,
  `end` int(11) NOT NULL,
  `distance` double NOT NULL default '0',
  KEY `start` (`start`),
  KEY `end` (`end`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
