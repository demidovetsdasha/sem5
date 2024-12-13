 CREATE TABLE Customers ( 
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,  
    CustomerType VARCHAR(50),  
    CustomerName VARCHAR(100) NOT NULL,  
    Address VARCHAR(255) NOT NULL,  
    DocumentSeries VARCHAR(50) NOT NULL,  
    DocumentNumber VARCHAR(50) NOT NULL,  
    BankName VARCHAR(100) NOT NULL,  
    BankNumber VARCHAR(20) NOT NULL, 
    CONSTRAINT UQ_Customer_Documents UNIQUE (DocumentSeries, DocumentNumber), 
    CONSTRAINT UQ_Customer_BankNumber UNIQUE (BankNumber)
); 

-- Таблица для хранения информации о пунктах назначения 
CREATE TABLE Destinations ( 
    DestinationID INT IDENTITY(1,1) PRIMARY KEY,  
    Town VARCHAR(100) NOT NULL,  
    Region VARCHAR(100) NOT NULL,  
    Country VARCHAR(100) NOT NULL,
    CONSTRAINT UQ_Customer_Address UNIQUE (Town, Region, Country) 
); 

-- Таблица для хранения информации о товарах 
CREATE TABLE Products ( 
    ProductID INT IDENTITY(1,1) PRIMARY KEY,  
    ProductName VARCHAR(100) NOT NULL,  
    ProductCategory VARCHAR(100) NOT NULL,
    ProductCode VARCHAR(50) UNIQUE NOT NULL, 

	CONSTRAINT UQ_Product UNIQUE (ProductName, ProductCategory) 
); 
 
-- Таблица для хранения информации о накладных 
CREATE TABLE Invoices ( 
    InvoiceID INT IDENTITY(1,1) PRIMARY KEY,  
    InvoiceDate DATE NOT NULL,  
    CustomerID INT NOT NULL,  
    DestinationID INT NOT NULL,  
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE ON UPDATE CASCADE,  
	FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID) ON DELETE CASCADE ON UPDATE CASCADE 
); 
 
-- Таблица для хранения информации о товарах в накладной 
CREATE TABLE InvoiceItems ( 
    InvoiceItemID INT IDENTITY(1,1) PRIMARY KEY,  
    InvoiceID INT NOT NULL,  
    ProductID INT NOT NULL,  
    Quantity INT NOT NULL CHECK (Quantity > 0),  
    ItemPrice DECIMAL(10, 2) NOT NULL CHECK (ItemPrice > 0),  
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID) ON DELETE CASCADE ON UPDATE CASCADE,  
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE ON UPDATE CASCADE, 
    CONSTRAINT UQ_InvoiceItems UNIQUE (InvoiceID, ProductID) 
); 
 

CREATE INDEX IDX_Customer_Name ON Customers(CustomerName); 
CREATE INDEX IDX_Destination_Town ON Destinations(Town); 
CREATE INDEX IDX_Product_Name ON Products(ProductName); 
CREATE INDEX IDX_Invoice_Date ON Invoices(InvoiceDate); 
CREATE INDEX IDX_InvoiceItems_Product ON InvoiceItems(ProductID); 
CREATE INDEX IDX_Product_Code ON Products(ProductCode);


-- Заполнение базовыми данными 
  
INSERT INTO Customers (CustomerType, CustomerName, Address, DocumentSeries, DocumentNumber, BankName, BankNumber) 
VALUES  
    ('Юридическое лицо', 'ООО Пример', N'Минск, ул. Независимости, 15', 'AB', '123456', 'Беларусбанк', '301234567890'), 
    ('Физическое лицо', 'Иван Иванов', 'Гомель, ул. Советская, 25', 'BC', '654321', 'Приорбанк', '301234567891'); 
 
INSERT INTO Destinations (Town, Region, Country) VALUES  
    ('Минск', 'Минская область', 'Беларусь'),  
    ('Москва', 'Москва', 'Россия'); 

INSERT INTO Products ( ProductName, ProductCategory, ProductCode) VALUES  
    ('Товар 1','Промышленные', 'PROD001'),  
    ('Товар 2', 'Бытовые', 'PROD002'),
    ('Товар 3', 'Торговое оборудование', 'PROD003'); 

INSERT INTO Invoices ( InvoiceDate, CustomerID, DestinationID) VALUES  
    ('2024-10-10', 1, 1),  
    ('2024-04-11', 2, 2),
    ('2024-04-20', 1, 1); 

INSERT INTO InvoiceItems ( InvoiceID, ProductID, Quantity, ItemPrice) VALUES  
    ( 1, 1, 5, 500.00),  
    (2, 2, 20, 25.00),
    (3, 3, 4, 2400.00); 


