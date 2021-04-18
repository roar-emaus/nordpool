import os
from pathlib import Path


_data_path = Path("data/elspot/")


def historic(from_year: int = 2021, to_year: int = 2021):
    if not from_year <= to_year:
        print("'from_year' needs to be smaller or equal to 'to_year'")
    else:
        template_url = (
            "https://www.nordpoolgroup.com/494bc9/globalassets/marketdata-excel-files/"
        )
        for year in range(from_year, to_year + 1):
            filename = f"elspot-prices_{year}_hourly_nok.xls"
            if (_data_path / filename).exists():
                os.system(f"rm {_data_path/filename}")
            os.system(f"wget -nv {template_url}{filename} -O {_data_path/filename}")
            os.system(
                f"unoconv -f csv -o {_data_path/str(year)}.csv {_data_path/filename}"
            )
            os.system(f"rm {_data_path/filename}")


def newest():
    data_url = (
        "https://www.nordpoolgroup.com/api/marketdata/page/23?currency=NOK,NOK,EUR,EUR"
    )
    os.system(f'wget -nv {data_url} -O {_data_path/"day_price.html"}')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download Day-Ahead elspot prices from Nordpool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--previous",
        help="Downloads historic data and converts it to csv files. [defaults: 2021 2021]",
        nargs="*",
        default=argparse.SUPPRESS,
        type=int,
    )
    parser.add_argument(
        "-n",
        "--newest",
        help="Downloads the newest day-ahead data",
        default=argparse.SUPPRESS,
        action="store_true",
    )

    args = vars(parser.parse_args())
    if args.get("previous", None) is not None:
        in_years = args["previous"]
        if len(in_years) == 0:
            historic()
        elif len(in_years) == 1:
            historic(from_year=in_years[0])
        elif len(in_years) == 2:
            historic(from_year=in_years[0], to_year=in_years[1])
        elif len(in_years) > 2:
            print("Only take 0 - 2 input year arguments, using the first two")
            historic(from_year=in_years[0], to_year=in_years[1])
    elif args.get("newest", None) is not None:
        newest()
