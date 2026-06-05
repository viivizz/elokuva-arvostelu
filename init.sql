DELETE FROM themes;
DELETE FROM styles;
DELETE FROM audiences;

INSERT INTO themes (value) VALUES ('dystopia');
INSERT INTO themes (value) VALUES ('utopia');
INSERT INTO themes (value) VALUES ('selviytyminen');
INSERT INTO themes (value) VALUES ('tulevaisuus');
INSERT INTO themes (value) VALUES ('historia');
INSERT INTO themes (value) VALUES ('sota');
INSERT INTO themes (value) VALUES ('avaruus');
INSERT INTO themes (value) VALUES ('rikollisuus');
INSERT INTO themes (value) VALUES ('tekoäly');
INSERT INTO themes (value) VALUES ('villilänsi');
INSERT INTO themes (value) VALUES ('ystävyys');
INSERT INTO themes (value) VALUES ('perhe');
INSERT INTO themes (value) VALUES ('politiikka');
INSERT INTO themes (value) VALUES ('katastrofi');
INSERT INTO themes (value) VALUES ('yliluonnollinen');


INSERT INTO styles (value) VALUES ('klassikko');
INSERT INTO styles (value) VALUES ('kulttielokuva');
INSERT INTO styles (value) VALUES ('indie');
INSERT INTO styles (value) VALUES ('taide-elokuva');
INSERT INTO styles (value) VALUES ('animaatio');
INSERT INTO styles (value) VALUES ('Oscar-voittaja');
INSERT INTO styles (value) VALUES ('blockbuster');
INSERT INTO styles (value) VALUES ('ikoninen');
INSERT INTO styles (value) VALUES ('visuaalinen');
INSERT INTO styles (value) VALUES ('realistinen');
INSERT INTO styles (value) VALUES ('dokumentti');
INSERT INTO styles (value) VALUES ('vähäeleinen');
INSERT INTO styles (value) VALUES ('minimalistinen');


INSERT INTO audiences (value) VALUES ('perhe');
INSERT INTO audiences (value) VALUES ('lapset');
INSERT INTO audiences (value) VALUES ('nuoret');
INSERT INTO audiences (value) VALUES ('aikuiset');
INSERT INTO audiences (value) VALUES ('kaikki');