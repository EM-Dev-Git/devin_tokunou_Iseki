# Database Documentation

## Stored Procedures

This directory contains the SQL stored procedures used by the IbUkeharai application for monthly and yearly data processing operations.

### Monthly Data Processing Procedures

- **Ukeharai.Select_Month_Data.txt** - Retrieves monthly update target data
- **Ukeharai.Update_Month_Data.txt** - Updates receipt/payment actual results (main error location)
- **Ukeharai.Update_Nengetu_Value.txt** - Updates year/month values in date management table

### Key Tables Referenced

- `Ukeharai.T_UKEHARAIJISSEKI` - Receipt/payment actual results table
- `Ukeharai.T_UKEHARAIMEISAI` - Receipt/payment detail table
- `Ukeharai.T_HIZUKE` - Date management table
- `Ukeharai.M_TORI` - Trading partner master table
- `Ukeharai.M_BUHIN` - Parts master table

### Error Investigation Notes

The monthly data processing error "受払実績情報の更新に失敗しました" occurs in the `Update_Month_Data` stored procedure, which:

1. Uses cursor operations to process each trading partner
2. Deletes existing records before inserting new ones
3. Performs complex joins between master and transaction tables
4. Operates within a transaction that rolls back on any error

Potential error causes:
- Data type conversion issues in cursor variables
- Foreign key constraint violations during INSERT
- Concurrent access conflicts during DELETE operations
- Invalid date range calculations affecting BETWEEN clauses
