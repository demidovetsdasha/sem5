
--Создание/удаление/редактирование товаров 

CREATE PROCEDURE AddProducts
    @ProductName VARCHAR(100), 
    @ProductCategory VARCHAR(50),
    @ProductCode VARCHAR(50)
AS
BEGIN
    INSERT INTO Products (ProductName, ProductCategory, ProductCode)
    VALUES (@ProductName, @ProductCategory, @ProductCode);
END;
GO


CREATE PROCEDURE EditProducts 
    @ProductCode VARCHAR(50), 
    @ProductName VARCHAR(100), 
    @ProductCategory VARCHAR(50)
AS
BEGIN
    UPDATE Products
    SET ProductName = @ProductName, 
        ProductCategory = @ProductCategory
    WHERE ProductCode = @ProductCode;
END;
GO


CREATE PROCEDURE DeleteProducts 
    @ProductCode VARCHAR(50)
AS
BEGIN
    DELETE FROM Products 
    WHERE ProductCode = @ProductCode;
END;
GO


--Создание/удаление/редактирование накладных

CREATE PROCEDURE AddInvoiceWithDetails
    @CustomerName NVARCHAR(100),
    @InvoiceDate DATE,
    @CustomerType NVARCHAR(50),
    @Price DECIMAL(10, 2),
    @ProductCode NVARCHAR(50),
    @Quantity INT,
    @Town NVARCHAR(100),
    @Region NVARCHAR(100),
    @Country NVARCHAR(100),
    @Address NVARCHAR(255),
    @DocumentSeries NVARCHAR(50),
    @DocumentNumber NVARCHAR(50),
    @BankNumber NVARCHAR(20),
    @BankName NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Поиск и создание покупателя
        DECLARE @CustomerID INT;
        SELECT @CustomerID = CustomerID
        FROM Customers
        WHERE DocumentSeries = @DocumentSeries
          AND DocumentNumber = @DocumentNumber;

        IF @CustomerID IS NULL
        BEGIN
            INSERT INTO Customers (CustomerType, CustomerName, Address, DocumentSeries, DocumentNumber, BankNumber, BankName)
            VALUES (@CustomerType, @CustomerName, @Address, @DocumentSeries, @DocumentNumber, @BankNumber, @BankName);

            SET @CustomerID = SCOPE_IDENTITY();
        END

        -- Поиск и создание пункта назначения
        DECLARE @DestinationID INT;
        SELECT @DestinationID = DestinationID
        FROM Destinations
        WHERE Town = @Town
          AND Region = @Region
          AND Country = @Country;

        IF @DestinationID IS NULL
        BEGIN
            INSERT INTO Destinations (Town, Region, Country)
            VALUES (@Town, @Region, @Country);

            SET @DestinationID = SCOPE_IDENTITY();
        END

        -- Создание накладной
        DECLARE @InvoiceID INT;
        INSERT INTO Invoices (InvoiceDate, CustomerID, DestinationID)
        VALUES (@InvoiceDate, @CustomerID, @DestinationID);

        SET @InvoiceID = SCOPE_IDENTITY();

        -- Получение ProductID для указанного ProductCode
        DECLARE @ProductID INT;
        SELECT @ProductID = ProductID
        FROM Products
        WHERE ProductCode = @ProductCode;

        IF @ProductID IS NULL
        BEGIN
            THROW 50000, 'Товар с указанным кодом не найден.', 1;
        END

        -- Добавление записи в InvoiceItems
        INSERT INTO InvoiceItems (InvoiceID, ProductID, Quantity, ItemPrice)
        VALUES (@InvoiceID, @ProductID, @Quantity, @Price);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO


CREATE FUNCTION GetInvoiceId
(
    @InvoiceDate DATE,
    @CustomerName NVARCHAR(100),
    @DestinationTown NVARCHAR(100)
)
RETURNS TABLE
AS
RETURN
(
    SELECT i.InvoiceID
  FROM Invoices i
  JOIN Customers c ON i.CustomerID = c.CustomerID
  JOIN Destinations d ON i.DestinationID = d.DestinationID
  WHERE i.InvoiceDate = @InvoiceDate
    AND c.CustomerName = @CustomerName
    AND d.Town = @DestinationTown
);
GO

CREATE PROCEDURE EditInvoice 
    @InvoiceID INT, 
    @InvoiceDate DATE, 
    @CustomerID INT, 
    @DestinationID INT
AS
BEGIN
    UPDATE Invoices
    SET InvoiceDate = @InvoiceDate, 
        CustomerID = @CustomerID, 
        DestinationID = @DestinationID
    WHERE InvoiceID = @InvoiceID;
END;
GO


CREATE PROCEDURE DeleteInvoice
    @InvoiceDate DATE,
    @CustomerName VARCHAR(100),
    @DestinationTown VARCHAR(100)
AS
BEGIN
    DELETE i
    FROM Invoices i
    JOIN Customers c ON i.CustomerID = c.CustomerID
    JOIN Destinations d ON i.DestinationID = d.DestinationID
    WHERE i.InvoiceDate = @InvoiceDate
      AND c.CustomerName = @CustomerName
      AND d.Town = @DestinationTown;
END;
GO


CREATE TRIGGER trg_DeleteInvoiceItems
ON Invoices
AFTER DELETE
AS
BEGIN
    DELETE FROM InvoiceItems
    WHERE InvoiceID IN (SELECT InvoiceID FROM DELETED);
END;
GO


CREATE PROCEDURE DeleteInvoice
    @InvoiceDate DATE,
    @CustomerName NVARCHAR(100),
    @DestinationTown NVARCHAR(100)
AS
BEGIN
    DELETE i
    FROM Invoices i
    JOIN Customers c ON i.CustomerID = c.CustomerID
    JOIN Destinations d ON i.DestinationID = d.DestinationID
    WHERE i.InvoiceDate = @InvoiceDate
      AND c.CustomerName = @CustomerName
      AND d.Town = @DestinationTown;
END;
GO


-- Функция для вывода макс.покупок пользователей по дате

CREATE FUNCTION GetTopCustomersByDate
(
    @InvoiceDate DATE
)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        i.InvoiceDate AS PurchaseDate,
        c.CustomerName,
        SUM(ii.Quantity * ii.ItemPrice) AS TotalPurchaseAmount
    FROM Invoices i
    JOIN Customers c ON i.CustomerID = c.CustomerID
    JOIN InvoiceItems ii ON i.InvoiceID = ii.InvoiceID
    WHERE i.InvoiceDate = @InvoiceDate
    GROUP BY i.InvoiceDate, c.CustomerName
    ORDER BY TotalPurchaseAmount DESC
);
GO


-- Функция для вывода изменений цены за определенный период

CREATE FUNCTION GetPriceChanges
(
    @ProductCode VARCHAR(50),
    @StartDate DATE,
    @EndDate DATE
)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        p.ProductName,
        c.CustomerName,
        i.InvoiceDate,
        ii.ItemPrice
    FROM Products p
    JOIN InvoiceItems ii ON p.ProductID = ii.ProductID
    JOIN Invoices i ON ii.InvoiceID = i.InvoiceID
    JOIN Customers c ON i.CustomerID = c.CustomerID
    WHERE p.ProductCode = @ProductCode
      AND i.InvoiceDate BETWEEN @StartDate AND @EndDate
);
GO


-- Функция для вывода всех категорий товаров

CREATE FUNCTION GetCategoriesUltra()
RETURNS TABLE
AS
RETURN
(
    SELECT 
        ProductCategory,
        ProductName,
        ProductCode
    FROM Products
);
GO

