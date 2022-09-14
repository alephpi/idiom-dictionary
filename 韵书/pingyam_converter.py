import pandas as pd
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

data = pd.read_csv('./pingyambiu.txt', sep='\t', header=None, usecols=[6, 7])
data.columns = ['粤拼', '广州拼音']


def converter(pingyam, from_style: Literal['粤拼', '广州拼音'] = '广州拼音', to_style: Literal['粤拼', '广州拼音'] = '粤拼'):
    item = data.query("{} == '{}'".format(from_style, pingyam))
    return item[to_style].iloc[0]
