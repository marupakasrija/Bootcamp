CREATE TABLE papers (
paper_id VARCHAR,
title VARCHAR,
abstract VARCHAR,
source_type VARCHAR,
created_at TIMESTAMP);

CREATE TABLE figures (
figure_id VARCHAR,
paper_id VARCHAR,
caption VARCHAR,
url VARCHAR,
created_at TIMESTAMP);

CREATE TABLE entities (
entity_id VARCHAR,
figure_id VARCHAR,
entity_type VARCHAR,
entity_text VARCHAR,
created_at TIMESTAMP);

INSERT INTO papers VALUES ('PMC2876325', 'S-layer stabilized lipid membranes (Review)', 'The present review focuses on a unique bio-molecular construction kit based on surface-layer (S-layer) proteins as building blocks and patterning elements, but also major classes of biological molecules such as lipids, membrane-active peptides and membrane proteins, and glycans for the design of functional supported lipid membranes. The biomimetic approach copying the supramolecular building principle of most archaeal cell envelopes merely composed of a plasma membrane and a closely associated S-layer lattice has resulted in robust and fluid lipid membranes. Most importantly, S-layer supported lipid membranes spanning an aperture or generated on solid and porous substrates constitute highly interesting model membranes for the reconstitution of responsive transmembrane proteins and membrane-active peptides. This is of particular challenge as one-third of all proteins are membrane proteins such as pore-forming proteins, ion channels, and receptors. S-layer supported lipid membranes are seen as one of the most innovative strategies in membrane protein-based nanobiotechnology with potential applications that range from pharmaceutical (high-throughput) drug screening over lipid chips to the detection of biological warfare agents.', 'pubmed', datetime.datetime(2025, 5, 17, 10, 57, 37, 852000));
