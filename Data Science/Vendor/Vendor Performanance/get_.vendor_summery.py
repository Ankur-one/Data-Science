import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db

logging.basicConfig(
    filename="logs/get_vendor_summery.log",
    level=logging.debug,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summery(conn):
    vendor_sales_summery = pd.read_sql_query("""with FreightSummery as (
        select
            VendorNumber,
            sum(Freight) as FreightCost
        from vendor_invoice
        group by VendorNumber
    );

    PurchaseSummery as ( 
        select
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
),

SalesSummery AS (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
)

    SELECT
        ps.VendorName,
        ps.VendorNumber,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummery ps
    LEFT JOIN SalesSummery ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummery fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """, conn)
    return vendor_sales_summery



def clean_data(df):
    df['Volume'] = df['Volume'].astype('float')
    df.fillna(0,inplace = True)

    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()


    vendor_sales_summery['GrossProfit'] = vendor_sales_summery['TotalSalesDollars'] - vendor_sales_summery['TotalPurchaseDollar']
    vendor_sales_summery['ProfitMargin'] = vendor_sales_summery['GrossProfit'] / vendor_sales_summery['TotalPurchaseDollar'] * 100
    vendor_sales_summery['StockTurnover'] = vendor_sales_summery['TotalSalesQuantity'] / vendor_sales_summery['TotalPurchaseDollar']
    vendor_sales_summery['SalesToPurchaseRatio'] = vendor_sales_summery['TotalSalesDollars'] / vendor_sales_summery['TotalPurchaseDollar']

    return df

if __name__ == "__main__":
    conn = sqlite3.connect('inventory.db')

    logging.info('creating Vendor Summery Table....')
    logging.info(summery_df.head())

    logging.info('Cleaning Data...')
    clean_df = clean_data(summery_df)
    logging.info(Clean_df.head())

    logging.info('Ingesting data...')
    ingest_db(clean_df, 'vendor_sales_summery',conn)
    logging.info('Completed')
            