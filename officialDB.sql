create database proyecto_personalizacion_articulos;
/*drop database proyecto_personalizacion_articulos;*/
use proyecto_personalizacion_articulos;

create table categorias(
idCate int auto_increment primary key not null,
nomCate varchar(50)
);

create table tela(
idTela int auto_increment primary key not null,
nomTela varchar(50)
);

    
    
insert into tela()
values(null,'Delgada'),
	(null,'Gruesa');
    
    
    
/*INSERT INTO cliente()
values(null,'Dan','Ala','danielala14fi@gmial.com','3014408183');
    
INSERT INTO pedido()
values(null,1,1,'10000','2023-06-08');


INSERT INTO productos()
values(null,1,1,'Small','Red','hola','hola2','Arial');*/
    


create table productos(
idPro int auto_increment primary key not null,
idRef int not null,
idPedido int not null,
talla varchar(20) not null,
color varchar(50) not null,
logo_delantero varchar(100) not null,
logo_trasero varchar(100) not null,
fuente varchar(100) not null
);


create table clientes(
idClie int auto_increment primary key not null,
nomClie varchar(50) not null,
apellidoCli varchar(50) not null,
email varchar(50) not null,
telClie varchar(20) not null,
usuario varchar(100) not null,
passw varchar(100) not null
);


create table pedido(
idPedido int primary key auto_increment not null,
idClie int not null,
idPro int not null,
valorFinal decimal,
fechaPedido date,
FOREIGN KEY (idClie) REFERENCES clientes(idClie)
);

create table referencias(
idRef int primary key auto_increment not null,
idCate int not null,
code varchar(100) not null,
nomRef varchar(70) not null,
precioRef decimal not null,
descripcionRef varchar(200),
idTela int not null,
img varchar(255)
);



alter table
referencias add foreign key(IdCate) references categorias(IdCate);

alter table
referencias add foreign key(IdTela) references tela(IdTela);

alter table
productos add foreign key(IdRef) references referencias(IdRef);

alter table
productos add foreign key(idPedido) references pedido(idPedido);



/*SELECTS*/
	
select*from categorias;
select*from referencias;
select*from clientes;
select*from productos;
select*from pedido;