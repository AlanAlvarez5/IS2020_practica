drop database if exists cinema;
create database if not exists cinema;

use cinema;

-- YYYY-MM-DD HH:MM:SS
create table if not exists usuario(
	id int not null auto_increment,
    nombre varchar(75) not null,
    correo varchar(30) not null,
    password varchar(8) not null,
    admin boolean not null,
    primary key (id)
)ENGINE = INNODB;

create table if not exists sala(
	id int not null auto_increment,
    n_filas int not null,
    n_asientos int not null,
    primary key (id)
) ENGINE = INNODB;

create table if not exists pelicula(
	id int not null auto_increment,
    nombre varchar(30) not null,
    descr varchar(256) not null,
    primary key(id)
)ENGINE = INNODB;

create table if not exists funcion(
	id int not null auto_increment,
    id_pelicula int not null,
    id_sala int not null,
    fecha_hora datetime not null,
    precio int not null,
	primary key(id),
    constraint fk_funcion_pelicula foreign key(id_pelicula)
		references pelicula(id)
        on delete cascade
        on update cascade,
	constraint fk_funcion_sala foreign key(id_sala)
		references sala(id)
        on delete cascade
        on update cascade
)ENGINE = INNODB;

create table if not exists compra(
	id int not null auto_increment,
    id_usuario int not null,
    fecha_hora datetime not null,
    total int not null,
    
    primary key(id),
    constraint fk_compra_usuario foreign key(id_usuario)
		references usuario(id)
        on delete cascade
        on update cascade
    
)ENGINE = INNODB;

create table if not exists asiento(
	id varchar(5) not null,
    id_funcion int not null,
    estado boolean not null,
    
    
    primary key(id, id_funcion),
    constraint fk_asiento_funcion foreign key(id_funcion)
		references funcion(id)
        on delete cascade
        on update cascade
    
)ENGINE = INNODB;

create table if not exists compra_asiento(
	id_compra int not null,
	id_asiento varchar(5) not null,
    id_funcion int not null,
    
    
    primary key(id_compra, id_asiento, id_funcion),
    constraint fk_ca_compra foreign key(id_compra)
		references compra(id)
        on delete cascade
        on update cascade,
    constraint fk_ca_asiento foreign key(id_asiento)
		references asiento(id)
        on delete cascade
        on update cascade,
    constraint fk_ca_funcion foreign key(id_funcion)
		references funcion(id)
        on delete cascade
        on update cascade
)ENGINE = INNODB;
