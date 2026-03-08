/* FILE_ID: LDD_ITW-1001.03-G.047-REF.001
DESCRIPTION: Logical Data Design for Customer Lifetime Value
*/

WITH Customer_Stats AS (
    SELECT 
        [Customer ID],
        [Customer Name],
        SUM([Sales]) AS Total_Revenue,
        SUM([Profit]) AS Total_Profit,
        COUNT(DISTINCT [Order ID]) AS Total_Orders,
        -- Calculate Customer Lifespan (CL) in years
        CASE 
            WHEN DATEDIFF(year, MIN([Order Date]), MAX([Order Date])) = 0 THEN 1 
            ELSE DATEDIFF(year, MIN([Order Date]), MAX([Order Date])) 
        END AS Lifespan_Years
    FROM [Sample - Superstore]
    GROUP BY [Customer ID], [Customer Name]
),
Metric_Components AS (
    SELECT 
        *,
        -- Average Order Value (AOV)
        Total_Revenue / NULLIF(Total_Orders, 0) AS AOV,
        -- Purchase Frequency (PF)
        Total_Orders / NULLIF(Lifespan_Years, 0) AS Purchase_Frequency,
        -- Profit Margin (PM) factor
        Total_Profit / NULLIF(Total_Revenue, 0) AS Profit_Margin
    FROM Customer_Stats
)
SELECT 
    [Customer ID],
    [Customer Name],
    ROUND(Total_Revenue, 2) AS Historical_Value,
    -- CLV Formula: (AOV * PF * CL * PM) 
    ROUND((AOV * Purchase_Frequency * Lifespan_Years * Profit_Margin), 2) AS Calculated_CLV
FROM Metric_Components
ORDER BY Calculated_CLV DESC;