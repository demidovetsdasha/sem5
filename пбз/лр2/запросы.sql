-- Функции и запросы 

-- 1. Список покупателей, сделавших покупку на максимальную сумму на определённую дату 
SELECT  
    i.InvoiceDate,  
    c.CustomerName,  
    c.Address,  
    SUM(ii.Quantity * ii.ItemPrice) AS TotalAmount 
FROM  
    Invoice i 
JOIN  
    Customer c ON i.CustomerID = c.CustomerID 
JOIN  
    InvoiceItems ii ON i.InvoiceID = ii.InvoiceID 
WHERE  
    i.InvoiceDate = '2023-10-28' 
GROUP BY  
    i.InvoiceDate, c.CustomerName, c.Address 
ORDER BY  
    TotalAmount DESC 
OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY; 
 
-- 2. Список изменений стоимости указанного товара за период времени 
SELECT  
    c.CustomerName AS Manufacturer,  
    p.ProductName,  
    i.InvoiceDate,  
    ii.ItemPrice AS Cost 
FROM  
    Invoice i 
JOIN  
    InvoiceItems ii ON i.InvoiceID = ii.InvoiceID 
JOIN  
    Product p ON ii.ProductID = p.ProductID 
JOIN  
    Customer c ON i.CustomerID = c.CustomerID 
WHERE  
    p.ProductName = N'Товар 1' AND  
    i.InvoiceDate BETWEEN '2023-01-01' AND '2023-12-31' 
ORDER BY  
    i.InvoiceDate; 
 
-- 3. Список существующих категорий товаров 
SELECT CategoryName FROM ProductCategory;