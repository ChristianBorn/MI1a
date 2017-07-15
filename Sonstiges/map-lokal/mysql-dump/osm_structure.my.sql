-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Erstellungszeit: 21. Mai 2017 um 11:40
-- Server-Version: 10.1.16-MariaDB
-- PHP-Version: 5.6.24

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Datenbank: `osm`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `members_nodes`
--
-- Erstellt am: 21. Mai 2017 um 04:31
--

DROP TABLE IF EXISTS `members_nodes`;
CREATE TABLE `members_nodes` (
  `node_id` bigint(20) NOT NULL,
  `relation_id` bigint(20) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `members_nodes`:
--   `node_id`
--       `nodes` -> `id`
--   `relation_id`
--       `relations` -> `id`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `members_relations`
--
-- Erstellt am: 21. Mai 2017 um 03:49
--

DROP TABLE IF EXISTS `members_relations`;
CREATE TABLE `members_relations` (
  `relation_id2` bigint(20) NOT NULL,
  `relation_id` bigint(20) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `members_relations`:
--   `relation_id`
--       `relations` -> `id`
--   `relation_id2`
--       `relations` -> `id`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `members_ways`
--
-- Erstellt am: 21. Mai 2017 um 03:50
--

DROP TABLE IF EXISTS `members_ways`;
CREATE TABLE `members_ways` (
  `way_id` bigint(20) NOT NULL,
  `relation_id` bigint(20) NOT NULL,
  `role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `members_ways`:
--   `relation_id`
--       `relations` -> `id`
--   `way_id`
--       `ways` -> `id`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nodes`
--
-- Erstellt am: 21. Mai 2017 um 05:54
--

DROP TABLE IF EXISTS `nodes`;
CREATE TABLE `nodes` (
  `id` bigint(20) NOT NULL,
  `lat` double NOT NULL,
  `lon` double NOT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `version` bigint(20) DEFAULT NULL,
  `changeset` bigint(20) DEFAULT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `nodes`:
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `nodes_tags`
--
-- Erstellt am: 21. Mai 2017 um 03:53
--

DROP TABLE IF EXISTS `nodes_tags`;
CREATE TABLE `nodes_tags` (
  `node_id` bigint(20) NOT NULL,
  `k` varchar(50) NOT NULL,
  `v` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `nodes_tags`:
--   `node_id`
--       `nodes` -> `id`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `relations`
--
-- Erstellt am: 21. Mai 2017 um 08:33
--

DROP TABLE IF EXISTS `relations`;
CREATE TABLE `relations` (
  `id` bigint(20) NOT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `version` bigint(20) DEFAULT NULL,
  `changeset` bigint(20) DEFAULT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `relations`:
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `relations_tags`
--
-- Erstellt am: 21. Mai 2017 um 03:55
--

DROP TABLE IF EXISTS `relations_tags`;
CREATE TABLE `relations_tags` (
  `relation_id` bigint(20) NOT NULL,
  `k` varchar(50) NOT NULL,
  `v` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `relations_tags`:
--   `relation_id`
--       `relations` -> `id`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ways`
--
-- Erstellt am: 21. Mai 2017 um 07:41
--

DROP TABLE IF EXISTS `ways`;
CREATE TABLE `ways` (
  `id` bigint(20) NOT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `version` bigint(20) DEFAULT NULL,
  `changeset` bigint(20) DEFAULT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `ways`:
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ways_nodes`
--
-- Erstellt am: 21. Mai 2017 um 03:58
--

DROP TABLE IF EXISTS `ways_nodes`;
CREATE TABLE `ways_nodes` (
  `node_id` bigint(20) NOT NULL,
  `way_id` bigint(20) NOT NULL,
  `sequence` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `ways_nodes`:
--   `node_id`
--       `nodes` -> `id`
--   `way_id`
--       `ways` -> `id`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ways_tags`
--
-- Erstellt am: 21. Mai 2017 um 03:57
--

DROP TABLE IF EXISTS `ways_tags`;
CREATE TABLE `ways_tags` (
  `way_id` bigint(20) NOT NULL,
  `k` varchar(50) NOT NULL,
  `v` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONEN DER TABELLE `ways_tags`:
--   `way_id`
--       `ways` -> `id`
--

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `members_nodes`
--
ALTER TABLE `members_nodes`
  ADD KEY `wayid` (`node_id`,`relation_id`);

--
-- Indizes für die Tabelle `members_relations`
--
ALTER TABLE `members_relations`
  ADD KEY `wayid` (`relation_id2`,`relation_id`);

--
-- Indizes für die Tabelle `members_ways`
--
ALTER TABLE `members_ways`
  ADD KEY `wayid` (`way_id`,`relation_id`);

--
-- Indizes für die Tabelle `nodes`
--
ALTER TABLE `nodes`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `nodes_tags`
--
ALTER TABLE `nodes_tags`
  ADD KEY `id` (`node_id`);

--
-- Indizes für die Tabelle `relations`
--
ALTER TABLE `relations`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `relations_tags`
--
ALTER TABLE `relations_tags`
  ADD KEY `id` (`relation_id`);

--
-- Indizes für die Tabelle `ways`
--
ALTER TABLE `ways`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `ways_nodes`
--
ALTER TABLE `ways_nodes`
  ADD KEY `nodeid` (`node_id`,`way_id`);

--
-- Indizes für die Tabelle `ways_tags`
--
ALTER TABLE `ways_tags`
  ADD KEY `id` (`way_id`);


--
-- Metadaten
--
USE `phpmyadmin`;

--
-- Metadaten für members_nodes
--

--
-- Metadaten für members_relations
--

--
-- Metadaten für members_ways
--

--
-- Metadaten für nodes
--

--
-- Metadaten für nodes_tags
--

--
-- Metadaten für relations
--

--
-- Metadaten für relations_tags
--

--
-- Metadaten für ways
--

--
-- Metadaten für ways_nodes
--

--
-- Metadaten für ways_tags
--

--
-- Metadaten für osm
--

--
-- Daten für Tabelle `pma__relation`
--

INSERT INTO `pma__relation` VALUES
('osm', 'members_nodes', 'node_id', 'osm', 'nodes', 'id'),
('osm', 'members_nodes', 'relation_id', 'osm', 'relations', 'id'),
('osm', 'members_relations', 'relation_id', 'osm', 'relations', 'id'),
('osm', 'members_relations', 'relation_id2', 'osm', 'relations', 'id'),
('osm', 'members_ways', 'relation_id', 'osm', 'relations', 'id'),
('osm', 'members_ways', 'way_id', 'osm', 'ways', 'id'),
('osm', 'nodes_tags', 'node_id', 'osm', 'nodes', 'id'),
('osm', 'relations_tags', 'relation_id', 'osm', 'relations', 'id'),
('osm', 'ways_nodes', 'node_id', 'osm', 'nodes', 'id'),
('osm', 'ways_nodes', 'way_id', 'osm', 'ways', 'id'),
('osm', 'ways_tags', 'way_id', 'osm', 'ways', 'id');
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
