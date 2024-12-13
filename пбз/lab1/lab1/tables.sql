CREATE TABLE поставщики (
    П VARCHAR(10) PRIMARY KEY,
    Имя_П VARCHAR(30) NOT NULL,
    Статус INT NOT NULL,
    Город VARCHAR(30) NOT NULL
);

CREATE TABLE детали (
    Д VARCHAR(10) PRIMARY KEY,
    Имя_Д VARCHAR(30) NOT NULL,
    Цвет VARCHAR(30) NOT NULL,
    Размер INTEGER NOT NULL,
    Город VARCHAR(30) NOT NULL
);

CREATE TABLE проекты (
    ПР VARCHAR(10) PRIMARY KEY,
    Имя_ПР VARCHAR(30) NOT NULL,
    Город VARCHAR(30) NOT NULL
);

CREATE TABLE поставки (
    П VARCHAR(10) NOT NULL,
    Д VARCHAR(10) NOT NULL,
    ПР VARCHAR(10) NOT NULL,
    S INTEGER NOT NULL,
    FOREIGN KEY (П) REFERENCES поставщики(П),
    FOREIGN KEY (Д) REFERENCES детали(Д),
    FOREIGN KEY (ПР) REFERENCES проекты(ПР)
);
