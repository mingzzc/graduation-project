create table book(
    id char(15) not null,
    title char(40) not null,
    picture char(200),
    info char(200),
    description char(200),
    label char(20),
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table evaluate(
    book_id char(15) not null,
    user_id char(30) not null,
    star char(20) not null,
    pos char(20),
    dat char(20),
    primary key(book_id,user_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table books(
    id char(15) not null,
    title varchar(40) not null,
    picture varchar(200),
    star char(3),
    author varchar(40),
    pub_site varchar(40),
    pub_time char(12),
    pages int,
    bind varchar(10),
    price varchar(20),
    info char(200),
    book_desc text,
    author_desc text,
    isbn char(20),
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table book_labels(
    book_id int not null,
    label_id int,
    primary key(book_id,label_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table labels(
    label_id int,
    lable char(20),
    primary key(label_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table users(
    id int auto_increment,
    username char(20) unique,
    password char(32),
    email char(30) unique,
    PRIMARY key(id)
)

create table mark(
    user_id int,
    book_id int,
    star int CHECK(star>=1 and star<=5),
    primary key(user_id,book_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;