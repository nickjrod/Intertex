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
@click.option('--left_file', '-i', required=True, help='Left file.')
@click.option('--right_file', '-v', required=True, help='Right file.')
@click.option('--left_column', required=True, help='Column to compare from left file.')
@click.option('--right_column', required=True, help='Column to compare from right file.')
@click.option('--comparison_type', type=click.Choice(['left', 'right', 'inner', 'outer'], case_sensitive=False))
def main(
	left_file: str, right_file: str, left_column:str, right_column: str, comparison_type: str
):
    """Compares the two files given based on the comparsion type passed in."""
    left_df = pd.read_excel(left_file)
    right_df = pd.read_excel(right_file)


    merged_df = itx_df.merge(vendor_df, how=comparison_type, left_on=left_column, right_on=right_column)

    now = datetime.now()
    current_time = now.strftime("%m-%d-%Y_%H;%M;%S")

    merged_df.to_excel(f"comparison_{comparison_type}_{current_time}.xlsx", index=False)


if __name__ == '__main__':
	main()