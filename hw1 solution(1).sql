BF768 Spring 2022
HW 1 Solution

-- 0. switch to a database
-- change to database of student
use username;

-- 1. Create table statements

drop table if exists game;
drop table if exists player;
drop table if exists team;
drop table if exists coach;

create table coach (
	cid integer not null auto_increment, 
	name varchar(30),
	contract_end date,
	primary key (cid)
) engine = innodb;

create table team (
	tid integer not null auto_increment, 
	team_name varchar(30),
	stadium varchar(30),
	city varchar(30),
	cid integer,
	primary key (tid),
	foreign key (cid) references coach (cid)	
) engine = innodb;

create table player (
    pid integer not null auto_increment,
    name varchar(30),
    number integer,
    position varchar(30),
    team integer not null,
    primary key (pid),
    foreign key (team) references team (tid)
) engine = innodb;

create table game (
	home_team integer not null,
	away_team integer not null,
	week integer,
	home_qb integer not null,
	away_qb integer not null,
	primary key (home_team, away_team),
	foreign key (home_team) references team (tid),
	foreign key (away_team) references team (tid),
	foreign key (home_qb) references player (pid),
	foreign key (home_qb) references player (pid)
) engine = innodb;


-- 2. Insert Statements go here
-- first possible method: using preassigned id values
insert into coach (cid, name, contract_end)
values
(1, 'Zac Taylor', '2022-04-01'),
(2, 'Sean McVay', '2022-04-01'), 
(3, 'Kyle Shanahan', '2022-04-01'),
(4, 'Robert Saleh', '2022-04-01');

insert into team (tid, team_name, stadium, city, cid)
values
(1, 'Bengals', 'Paul Brown Stadium', 'Cincinnati', 1),
(2, 'Rams', 'SoFi Stadium', 'Los Angeles', 2),
(3, '49ers', "Levi's Stadium", 'San Francisco', 3),
(4, 'Jets', 'Met Life Stadium', 'New York', 4);

insert into player (pid, name, number, position, team)
values
(1, 'Joe Burrow', 9, 'QB', 1),
(2, 'Matthew Stafford', 9, 'QB', 2),
(3, 'Trey Lance', 5, 'QB', 3),
(4, 'Zach Wilson', 2, 'QB', 4),
(5, 'Bryce Hall', 34, 'CB', 4),
(6, 'Kyle Juszczyk', 44, 'FB', 3),
(7, 'Kendall Blanton', 86, 'TE', 2),
(8, 'Jonah Williams', 73, 'OL', 1);

insert into game (home_team, away_team, week, home_qb, away_qb)
values
(1,2,1,1,2),
(3,4,2,3,4),
(1,3,3,1,3);

-- 3. Select statements
-- a) List all teams (team_name, stadium, city).
select team_name, stadium, city
from team;

-- b) List all quarterbacks (name, number). 
select name, number 
from player 
where position = 'QB';

-- c). List each coach (name, team, contract_end) in descending order by contract end date. 
select name, team_name, contract_end
from coach join team using (cid)
order by contract_end desc;

-- d) List all players (name, position, team_name) in alphabetical order by team name and then player name.
select name, position, team_name
from player join team using(tid)
order by team_name asc, name asc;


-- e) List each game (home team name, away team name, stadium, week) in order by week ascending. 
select h.team_name, a.team_name stadium, week
from game join team as h on home_team=h.tid join team as a on away_team=a.tid
order by week asc;

