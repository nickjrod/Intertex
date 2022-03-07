import numpy as np
import click
import pandas as pd
from datetime import datetime


NEW_PRICE = 'new_price'
OLD_PRICE = 'old_price'
PERCENT = 'percentage_chage'


def create_output_df(merged_df, itx_sku_c, itx_price_c, vendor_price_c):
	"""Calculates the values for the output file."""
	merged_df[PERCENT] = ((merged_df[vendor_price_c] - merged_df[itx_price_c]) / merged_df[itx_price_c])*100
	return merged_df[[itx_sku_c, itx_price_c, vendor_price_c, PERCENT]]


@click.command()
@click.option('--intertex_file', '-i', required=True, help='File that contains intertex data.')
@click.option('--vendor_file', '-v', required=True, help='File that contains vendor data.')
@click.option('--itx_sku_c', required=True, help='Sku column name in the intertex_file.')
@click.option('--vendor_sku_c', required=True, help='Sku column name in the vendor_file.')
@click.option('--itx_price_c', required=True, help='Price column name in the intertex_file.')
@click.option('--vendor_price_c', required=True, help='Price column name in the vendor_file.')
def main(
	intertex_file: str, vendor_file: str, itx_sku_c: str, itx_price_c: str, vendor_sku_c: str, vendor_price_c
):
    """Updates the prices associated with skus from the intertex file that match with skus in the vendor file."""
    itx_df = pd.read_excel(intertex_file)
    vendor_df = pd.read_excel(vendor_file)

    if itx_price_c == vendor_price_c:
    	updated_column_name = vendor_price_c + '_vendor'
    	vendor_df.rename(columns={vendor_price_c: updated_column_name})
    	vendor_price_c = updated_column_name

    merged_df = itx_df.merge(vendor_df, how='inner', left_on=itx_sku_c, right_on=vendor_sku_c)
    output_df = create_output_df(merged_df, itx_sku_c, itx_price_c, vendor_price_c)

    # # update the prices
    updated_df = itx_df.merge(vendor_df[[vendor_sku_c, vendor_price_c]], how='left', left_on=itx_sku_c, right_on=vendor_sku_c)
    updated_df[itx_price_c] = updated_df[vendor_price_c].fillna(updated_df[itx_price_c])
    updated_df = updated_df.drop([vendor_sku_c, vendor_price_c], axis=1)

    now = datetime.now()
    current_time = now.strftime("%m-%d-%Y_%H;%M;%S")

    updated_df.to_excel(f"{intertex_file.split('.')[0]}_{current_time}.xlsx", index=False)
    output_df.rename(columns={itx_price_c: OLD_PRICE, vendor_price_c: NEW_PRICE})
    output_df.to_excel(f"flagged_{current_time}.xlsx")


if __name__ == '__main__':
	main()