/* ITW_ID: itw_1001.03.G.047-REF.001
   METRIC: Customer Lifetime Value (CLV)
   FRAMEWORK: Logic RFC (IfThenWhy)
*/

WITH core_events AS (
    -- THE 'IF': Capturing only valid revenue-generating events
    -- DIC Rule: Exclude if transaction_history is NULL
    SELECT 
        c.Customer_ID,
        o.Order_ID,
        o.Order_Date,
        t.Sales,
        p.Product_Cost,
        o.Shipping_Cost
    FROM Customers c
    INNER JOIN Orders o ON c.Customer_ID = o.Customer_ID
    INNER JOIN Transactions t ON o.Order_ID = t.Order_ID
    INNER JOIN Products p ON t.Product_ID = p.Product_ID
    WHERE t.Sales > 0 -- LDD Validation Rule
),

metric_components AS (
    -- THE 'THEN': Logical Data Design (LDD) Equations
    SELECT 
        Customer_ID,
        -- AOV: Average Order Value
        (SUM(Sales) / COUNT(DISTINCT Order_ID)) AS AOV,
        
        -- CL: Customer Lifespan (Yearly difference or 1 if same year)
        CASE 
            WHEN DATEDIFF('year', MIN(Order_Date), MAX(Order_Date)) = 0 THEN 1 
            ELSE DATEDIFF('year', MIN(Order_Date), MAX(Order_Date)) 
        END AS CL,
        
        -- PF: Purchase Frequency (Orders per Year)
        COUNT(DISTINCT Order_ID) / 
            NULLIF(CASE 
                WHEN DATEDIFF('year', MIN(Order_Date), MAX(Order_Date)) = 0 THEN 1 
                ELSE DATEDIFF('year', MIN(Order_Date), MAX(Order_Date)) 
            END, 0) AS PF,
            
        -- PM: Profit Margin (Sales - Costs) / Sales
        (SUM(Sales) - (SUM(Product_Cost) + SUM(Shipping_Cost))) / NULLIF(SUM(Sales), 0) AS PM
    FROM core_events
    GROUP BY Customer_ID
)

-- THE 'WHY': Strategic Intent - Measuring Long-term Value
SELECT 
    Customer_ID,
    AOV,
    PF,
    CL,
    PM,
    -- FINAL CALCULATION: AOV * PF * CL * PM
    (AOV * PF * CL * PM) AS Customer_Lifetime_Value
FROM metric_components
WHERE (AOV * PF * CL * PM) > 0; -- LDD Validation: CLV > 0