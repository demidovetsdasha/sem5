-- Таблица для хранения информации о покупателях
CREATE TABLE Customer ( 
    CustomerID INT PRIMARY KEY, 
    CustomerType VARCHAR(50), 
    CustomerName VARCHAR(100) NOT NULL, 
    Address VARCHAR(255) NOT NULL, 
    DocumentSeries VARCHAR(50) NOT NULL, 
    DocumentNumber VARCHAR(50) NOT NULL, 
    BankName VARCHAR(100) NOT NULL, 
    BankNumber VARCHAR(20) NOT NULL 
); 
 
-- Таблица для хранения информации о пунктах назначения 
CREATE TABLE Destination ( 
    DestinationID INT PRIMARY KEY, 
    Town VARCHAR(100) NOT NULL, 
    Region VARCHAR(100) NOT NULL, 
    Country VARCHAR(100) NOT NULL 
); 
 
-- Таблица для хранения информации о категориях товаров 
CREATE TABLE ProductCategory ( 
    CategoryID INT PRIMARY KEY, 
    CategoryName VARCHAR(100) UNIQUE NOT NULL 
); 
 
-- Таблица для хранения информации о товарах 
CREATE TABLE Product ( 
    ProductID INT PRIMARY KEY, 
    ProductName VARCHAR(100) NOT NULL, 
    CategoryID INT NOT NULL, 
    FOREIGN KEY (CategoryID) REFERENCES ProductCategory(CategoryID) ON DELETE SET NULL ON UPDATE CASCADE 
); 
 
-- Таблица для хранения информации о накладных 
CREATE TABLE Invoice ( 
    InvoiceID INT PRIMARY KEY, 
    InvoiceDate DATE NOT NULL, 
    CustomerID INT NOT NULL, 
    DestinationID INT NOT NULL, 
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (DestinationID) REFERENCES Destination(DestinationID) ON DELETE SET NULL ON UPDATE CASCADE 
); 
 
-- Таблица для хранения информации о товарах в накладной 
CREATE TABLE InvoiceItems ( 
    InvoiceItemID INT PRIMARY KEY, 
    InvoiceID INT NOT NULL, 
    ProductID INT NOT NULL, 
    Quantity INT NOT NULL CHECK (Quantity > 0), 
    ItemPrice DECIMAL(10, 2) NOT NULL CHECK (ItemPrice > 0), 
    FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceID) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE ON UPDATE CASCADE
); 

-- Заполнение базовыми данными 
 
-- Категории товаров 
INSERT INTO ProductCategory (CategoryID, CategoryName) VALUES  
    (1, 'Промышленные'),  
    (2, 'Бытовые'),  
    (3, 'Торговое оборудование'); 
 
-- Покупатели 
INSERT INTO Customer (CustomerID, CustomerType, CustomerName, Address, DocumentSeries, DocumentNumber, BankName, BankNumber) 
VALUES  
    (1, 'Юридическое лицо', 'ООО Пример', N'Минск, ул. Независимости, 15', 'AB', '123456', 'Беларусбанк', '301234567890'), 
    (2, 'Физическое лицо', 'Иван Иванов', 'Гомель, ул. Советская, 25', 'BC', '654321', 'Приорбанк', '301234567891'); 
 
-- Пункты назначения 
INSERT INTO Destination (DestinationID, Town, Region, Country) VALUES  
    (1, 'Минск', 'Минская область', 'Беларусь'),  
    (2, 'Москва', 'Москва', 'Россия'); 
 
-- Товары 
INSERT INTO Product (ProductID, ProductName, CategoryID) VALUES  
    (1, 'Товар 1', 1),  
    (2, 'Товар 2', 2); 
 
-- Накладные 
INSERT INTO Invoice (InvoiceID, InvoiceDate, CustomerID, DestinationID) VALUES  
    (1, '2023-10-28', 1, 1),  
    (2, '2023-10-29', 2, 2); 
 
-- Позиции в накладных 
INSERT INTO InvoiceItems (InvoiceItemID, InvoiceID, ProductID, Quantity, ItemPrice) VALUES  
    (1, 1, 1, 10, 500.00),  
    (2, 2, 2, 5, 1500.00); 


