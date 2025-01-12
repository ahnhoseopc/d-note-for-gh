--
-- RUN AS SYSTEM
--
-- CREATE USER hoseop IDENTIFIED BY "mypasswd!@";
-- GRANT CREATE SESSION TO hoseop;
-- GRANT CREATE TABLE TO hoseop;
-- ALTER USER hoseop QUOTA UNLIMITED ON users;

--
-- RUN AS HOSEOP
--
create table mytbl (col1 VARCHAR2(20), col2 NUMBER(18,6));
INSERT INTO mytbl (col1, col2) VALUES ('가나다', 123.456);
INSERT INTO mytbl (col1, col2) VALUES ('라마바', 789.012);
INSERT INTO mytbl (col1, col2) VALUES ('사아자', 456.789);
INSERT INTO mytbl (col1, col2) VALUES ('차카타', 101.112);
INSERT INTO mytbl (col1, col2) VALUES ('파하', 12.123);
INSERT INTO mytbl (col1, col2) VALUES ('ABCDEF', 987.654);
INSERT INTO mytbl (col1, col2) VALUES ('GHIJKL', 321.098);
INSERT INTO mytbl (col1, col2) VALUES ('MNOPQR', 654.321);
INSERT INTO mytbl (col1, col2) VALUES ('STUVWX', 98.765);
INSERT INTO mytbl (col1, col2) VALUES ('YZ', 43.210);
COMMIT;
select * from mytbl;
select * from all_tables;


