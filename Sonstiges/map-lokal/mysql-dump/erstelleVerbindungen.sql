-- SRC: http://goblor.de/wp/2009/10/17/openstreetmap-projekt-teil2-%e2%80%93-von-den-rohdaten-zum-gerichteten-graphen/
DELIMITER $$

DROP PROCEDURE IF EXISTS `erstelleVerbindungen`$$
CREATE PROCEDURE `erstelleVerbindungen`()

BEGIN

DECLARE startnode bigint(20);
DECLARE lastlon double;
DECLARE lastlat double;
DECLARE endnode bigint(20);
DECLARE wayid bigint(20);
DECLARE distance double DEFAULT 0;
DECLARE adddist double;
DECLARE oneway BOOLEAN DEFAULT FALSE;
DECLARE lastwayid bigint(20);

DECLARE nodecount INT DEFAULT 0;

DECLARE readwayid bigint(20);
DECLARE readnodeid bigint(20);
DECLARE readsequence int(32);
DECLARE readlat double;
DECLARE readlon double;
DECLARE readoneway BOOLEAN;

DECLARE finished BOOLEAN DEFAULT 0;

DECLARE waycur CURSOR FOR
SELECT distinct ways_tags.way_id as wayid, ways_nodes.node_id as nodeid,
    ways_nodes.sequence as sequence, nodes.lat as lat,
    nodes.lon as lon, (w.k="oneway" and w.v="yes") as oneway
FROM ways_tags
    INNER JOIN ways_nodes on ways_nodes.way_id = ways_tags.way_id
    INNER JOIN nodes on ways_nodes.node_id = nodes.id
    LEFT JOIN ways_tags as w on ways_tags.way_id = w.way_id and w.k="oneway"
WHERE ways_tags.k ="highway" and
    (ways_tags.v="living_street"
    or ways_tags.v="motorway"
    or ways_tags.v="motorway_link"
    or ways_tags.v="primary"
    or ways_tags.v="primary_link"
    or ways_tags.v="residential"
    or ways_tags.v="secondary"
    or ways_tags.v="secondary_link"
    or ways_tags.v="tertiary"
    or ways_tags.v="tertiary_link"
    or ways_tags.v="trunk"
    or ways_tags.v="trunk_link")
ORDER BY ways_tags.way_id, ways_nodes.sequence;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

OPEN waycur;

SELECT 0 INTO wayid;

CREATE TEMPORARY TABLE `temp_autonodecount` (
    `count` int(11) NOT NULL,
    `nodeid` bigint(20) NOT NULL,
    PRIMARY KEY  (`nodeid`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;

INSERT INTO temp_autonodecount(count, nodeid)
    SELECT COUNT(ways_nodes.node_id), ways_nodes.node_id
    FROM ways_tags
        INNER JOIN ways_nodes on ways_nodes.way_id = ways_tags.way_id
    WHERE ways_tags.k ="highway" and
        (ways_tags.v="living_street"
        or ways_tags.v="motorway"
        or ways_tags.v="motorway_link"
        or ways_tags.v="primary"
        or ways_tags.v="primary_link"
        or ways_tags.v="residential"
        or ways_tags.v="secondary"
        or ways_tags.v="secondary_link"
        or ways_tags.v="tertiary"
        or ways_tags.v="tertiary_link"
        or ways_tags.v="trunk"
        or ways_tags.v="trunk_link")
    GROUP BY ways_nodes.node_id
    HAVING count(ways_nodes.node_id)>1;

FETCH waycur INTO readwayid, readnodeid, readsequence, readlat, readlon, readoneway;

WHILE NOT finished DO
    IF readsequence <> 1 THEN
        SELECT
            acos(sin(readlat*PI()/180)*sin(lastlat*PI()/180)+cos(readlat*PI()/180)*cos(lastlat*PI()/180)*cos((lastlon-readlon)*PI()/180))*6370
                INTO adddist;
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
        SELECT count INTO nodecount FROM temp_autonodecount WHERE temp_autonodecount.nodeid=endnode;
        SELECT 0 INTO finished;
    END IF;

    FETCH waycur INTO readwayid, readnodeid, readsequence, readlat, readlon, readoneway;

    IF (wayid <> readwayid OR readsequence IS NULL OR nodecount > 1) THEN
        IF (lastwayid=wayid) THEN
            INSERT INTO verbindungen(wayid, start, end, distance)
            VALUES (wayid, startnode, endnode, distance);
            IF oneway = 0 or oneway is NULL THEN
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

DROP TABLE `temp_autonodecount`;

END$$
DELIMITER ;
