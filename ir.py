import sys
import argparse
import datetime
from dateutil.relativedelta import relativedelta

from src.stuff import get_operations_dataframe, calcula_custodia, vendas_no_mes


def main(raw_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', required=False)
    args = parser.parse_args(raw_args)

    if args.do == 'custodia':
        do_custodia()
        return

    if args.do == 'vendas_no_mes':
        do_vendas_no_mes()
        return

    do_vendas_no_mes()

def do_custodia():
    from src.dropbox_files import download_dropbox_file
    download_dropbox_file()
    print(calcula_custodia(get_operations_dataframe()))

def do_vendas_no_mes():
    from src.dropbox_files import download_dropbox_file
    download_dropbox_file()

    df = get_operations_dataframe()

    data = df['data'].min()
    hoje = datetime.datetime.now().date()
    datas = []

    while data < hoje:
        datas.append(data)
        data = data + relativedelta(months=1)

    datas.append(hoje)

    for data in datas:
        print('Mes: ' + str(data.month) + ' Ano: ' + str(data.year))
        print(vendas_no_mes(df, data.year, data.month))

if __name__ == "__main__":
    main(sys.argv[1:])