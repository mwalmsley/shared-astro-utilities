

from astropy.table import Table

from time_utils import current_time


def cache_table(table_loc, cache_loc, useful_cols, loading_func=Table.read, kwargs=None):
    """
    Save a column subset of astropy.table. This can be read later to save time.
    Args:
        table_loc (str): file location of astropy.table to load
        cache_loc (str): file location to save column subset of astropy.table
        useful_cols (list): of form ['a_column_to_save', ...]
        loading_func (func): function to load table, where first arg is table_loc
        kwargs (dict): (optional) additional keyword arguments for loading_func

    Returns:
        None
    """
    print('Begin caching at {}'.format(current_time()))
    data = loading_func(table_loc, **kwargs)
    print('Table loaded at {}'.format(current_time()))
    data[useful_cols].write(cache_loc, overwrite=True)
    print('Saved to astropy.Table at {}'.format(current_time()))


def astropy_table_to_pandas(table):
    """
    Convert astropy table to pandas
    Wrapper for table.to_pandas() that automatically avoids multidimensional columns
    Note that the reverse is already implemented: Table.from_pandas(df)
    Args:
        table (astropy.Table): table to be converted to pandas

    Returns:
        (pd.DataFrame) original table as DataFrame, excluding multi-dim columns
    """
    for col in table.colnames:
        # if it has a shape
        try:
            exists = table[col].shape[1]
        except IndexError:
            print('{} is already one-dim'.format(col))
        else:
            print('converting {}'.format(col))
            col_values = table[col]
            #  convert to string
            col_strings = list(map(lambda x: str(list(x)), col_values))
            # replace original values
            table[col] = col_strings

    df = table.to_pandas()
    return df
