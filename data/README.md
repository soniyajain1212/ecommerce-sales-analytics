# Data Directory

## Dataset Information

**Source**: Simulated e-commerce transaction data  
**Records**: 50,000+ transactions  
**Time Period**: 2 years (2022-2024)  

### Schema
- Order_ID: Unique transaction identifier
- Customer_ID: Unique customer identifier
- Date: Transaction timestamp
- Category: Product category
- Price: Unit price
- Quantity: Items purchased
- Revenue: Total transaction value
- Customer_Segment: Customer tier (Premium/Regular/Budget)
- Region: Geographic region

### Data Generation
Data was generated using Python's NumPy random functions to simulate realistic e-commerce patterns including:
- Seasonal variations
- Customer behavior patterns
- Regional distribution
- Category preferences

### Note
Actual CSV file not included due to size. Run `ecommerce_analysis.py` to generate fresh dataset.
