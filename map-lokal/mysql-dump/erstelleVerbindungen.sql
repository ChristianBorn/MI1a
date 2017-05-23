-- SRC: http://goblor.de/wp/2009/10/17/openstreetmap-projekt-teil2-%e2%80%93-von-den-rohdaten-zum-gerichteten-graphen/
DELIMITER $$

DROP PROCEDURE IF EXISTS `osm`.`erstelleVerbindungen`$$
CREATE DEFINER=`osm`@`localhost` PROCEDURE `erstelleVerbindungen`()
BEGIN

DECLARE startnode int(32);
DECLARE lastlon double;
DECLARE lastlat double;
DECLARE endnode int(32);
DECLARE wayid int(32);
DECLARE distance double DEFAULT 0;
DECLARE adddist double;
DECLARE oneway BOOLEAN DEFAULT FALSE;
DECLARE lastwayid int(32);

DECLARE nodecount INT DEFAULT 0;

DECLARE readwayid int(32);
DECLARE readnodeid int(32);
DECLARE readsequence int(32);
DECLARE readlat double;
DECLARE readlon double;
DECLARE readoneway BOOLEAN;

DECLARE finished BOOLEAN DEFAULT 0;

DECLARE waycur CURSOR FOR
SELECT distinct way_tags.id as wayid, ways_nodes.nodeid as nodeid, ways_nodes.sequence as sequence, nodes.lat as lat, nodes.lon as lon, (w.k="oneway" and w.v="yes") as oneway
FROM way_tags
INNER JOIN ways_nodes on ways_nodes.wayid = way_tags.id
INNER JOIN nodes on ways_nodes.nodeid = nodes.id
left join way_tags as w on way_tags.id = w.id and w.k="oneway"
WHERE way_tags.k ="highway" and
	(way_tags.v="living_street"
	or way_tags.v="motorway"
	or way_tags.v="motorway_link"
	or way_tags.v="primary"
	or way_tags.v="primary_link"
	or way_tags.v="residential"
	or way_tags.v="secondary"
	or way_tags.v="secondary_link"
	or way_tags.v="tertiary"
	or way_tags.v="tertiary_link"
	or way_tags.v="trunk"
	or way_tags.v="trunk_link")
ORDER BY way_tags.id, ways_nodes.sequence;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

OPEN waycur;

SELECT 0 INTO wayid;

CREATE TEMPORARY TABLE  `osm`.`temp_autonodecount` (
  `count` int(11) NOT NULL,
  `nodeid` int(11) NOT NULL,
  PRIMARY KEY  (`nodeid`)
) ENGINE=MEMORY DEFAULT CHARSET=latin1;

INSERT INTO temp_autonodecount(count, nodeid)
SELECT COUNT(ways_nodes.nodeid), ways_nodes.nodeid
FROM way_tags
INNER JOIN ways_nodes on ways_nodes.wayid = way_tags.id
WHERE way_tags.k ="highway" and
	(way_tags.v="living_street"
	or way_tags.v="motorway"
	or way_tags.v="motorway_link"
	or way_tags.v="primary"
	or way_tags.v="primary_link"
	or way_tags.v="residential"
	or way_tags.v="secondary"
	or way_tags.v="secondary_link"
	or way_tags.v="tertiary"
	or way_tags.v="tertiary_link"
	or way_tags.v="trunk"
	or way_tags.v="trunk_link")
GROUP BY nodeid
HAVING count(nodeid)>1;

FETCH waycur INTO readwayid, readnodeid, readsequence, readlat, readlon, readoneway;

WHILE NOT finished DO
	if readsequence <> 1 THEN
		SELECT acos(sin(readlat*PI()/180)*sin(lastlat*PI()/180)+cos(readlat*PI()/180)*cos(lastlat*PI()/180)*cos((lastlon-readlon)*PI()/180))*6370 INTO adddist;
		IF NOT adddist IS NULL THEN
			SELECT distance+adddist INTO distance;
		END IF;
	END IF;

	IF wayid <> readwayid THEN
		SELECT readoneway INTO oneway;
		SELECT readnodeid INTO startnode;
		SELECT readlat INTO lastlat;
		SELECT readlon INTO lastlon;
		SELECT wayid INTO lastwayid;
		SELECT readwayid INTO wayid;
		SELECT 0 INTO nodecount;
	ELSE
		SELECT readoneway INTO oneway;
		SELECT readlat INTO lastlat;
		SELECT readlon INTO lastlon;
		SELECT readnodeid INTO endnode;
		SELECT wayid INTO lastwayid;

		SELECT count
		INTO nodecount
		FROM temp_autonodecount
		WHERE temp_autonodecount.nodeid=endnode;
		select 0 into finished;
	END IF;

	FETCH waycur INTO readwayid, readnodeid, readsequence, readlat, readlon, readoneway;

	IF (wayid <> readwayid OR readsequence IS NULL OR nodecount > 1) THEN
		IF (lastwayid=wayid) THEN
			INSERT INTO verbindungen(wayid, start, end, distance)
			VALUES (wayid, startnode, endnode, distance);
			if oneway = 0 or oneway is NULL then
				INSERT INTO verbindungen(wayid, start, end, distance)
				VALUES (wayid, endnode, startnode, distance);
			end if;
		END IF;

		SELECT 0 INTO distance;
	END IF;
	IF nodecount > 1 THEN
		SELECT endnode INTO startnode;
	END IF;
END WHILE;

DROP TABLE `osm`.`temp_autonodecount`;

END$$

DELIMITER ;

