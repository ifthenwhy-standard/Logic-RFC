/* FILE_ID: LDD_ITW-1001.03-G.047-REF.sql
DESCRIPTION: Logical Data Design for Customer Lifetime Value
*/

WITH Customer_Stats AS (
    SELECT 
        [Customer ID],
        [Customer Name],
        SUM(Sales) AS Total_Revenue,
        COUNT(DISTINCT [Order ID]) AS Total_Orders,
        -- Calculate Customer Lifespan in years
        DATEDIFF(day, MIN([Order Date]), MAX([Order Date])) / 365.0 AS Lifespan_Years
    FROM [Sample - Superstore]
    GROUP BY [Customer ID], [Customer Name]
),
Metric_Components AS (
    SELECT 
        *,
        -- Average Order Value (AOV)
        Total_Revenue / NULLIF(Total_Orders, 0) AS AOV,
        -- Purchase Frequency (Orders per Year)
        Total_Orders / NULLIF(Lifespan_Years, 0) AS Purchase_Frequency
    FROM Customer_Stats
)
SELECT 
    [Customer ID],
    [Customer Name],
    ROUND(Total_Revenue, 2) AS Historical_Value,
    -- CLV Formula: (AOV * Purchase_Frequency) * Lifespan
    -- Note: For this dataset, Historical Revenue is our current Ground Truth for CLV
    ROUND((AOV * Purchase_Frequency) * Lifespan_Years, 2) AS Calculated_CLV
FROM Metric_Components
ORDER BY Calculated_CLV DESC;