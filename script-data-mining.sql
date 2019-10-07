-- Database: DataMining

-- DROP DATABASE "DataMining";

CREATE DATABASE "DataMining"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	

create table transacoes(
	tid serial primary key,
	leite bool not null,
	cafe bool not null,
	cerveja bool not null,
	pao bool not null,
	manteiga bool not null,
	arroz bool not null,
	feijao bool not null
)

select * from transacoes;
drop table transacoes;
delete from transacoes;

--1
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,true,false,true,true,false,false);
--2
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(true,false,true,true,true,false,false);
--3
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,true,false,true,true,false,false);
--4
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(true,true,false,true,true,false,false);
--5
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,false,true,false,false,false,false);
--6
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,false,false,false,true,false,false);
--7
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,false,false,true,false,false,false);
--8
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,false,false,false,false,false,true);
--9
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,false,false,false,false,true,true);
--10
insert into transacoes(leite, cafe, cerveja, pao, manteiga, arroz, feijao) values
(false,false,false,false,false,true,false);