# Import other/growingseason.csv
import pandas as pd

def get_growing_season():
    growing_season = pd.read_csv('other/growingseason.csv')
    return growing_season

df = get_growing_season()

# 1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022
# 181.55,182.31,182.39,184.2,182.87,184.97,183.58,182.82,181.45,181.25,182.7,181.16,181.15,183.36,186.83,182.26,181.61,184.95,182.35,181.84,181.99,181.25,183.12,181.42,182.55,181.61,182.86,183.82,181.87,182.18,185.91,182.74,181.14,181.64,182.23,181.1,181.21,181.42,182.54,182.77,186.77,181.24,184.74,181.7,187.19,182.05,183.33,185.67,182.34,181.09,182.24,185.75,183.68,181.59,183.18,181.73,181.69,184.21,183.56,182.58,181.03,186.12,182.14,181.42,181.24,181.22,182.26,181.08,181.23,181.09,182.18,181.07,181.17

# Should be year,gdd
# 1950,181.55
# 1951,182.31
# 1952,182.39
# 1953,184.2

# Transpose the dataframe
df = df.T

# Reset the index
df = df.reset_index()

# Rename the columns
df.columns = ['year', 'gdd']

print(df)

# Save the dataframe to a csv file
df.to_csv('other/growing_season.csv', index=False)