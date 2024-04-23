import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split

train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

train.drop(columns="id", axis=1, inplace=True)
test.drop(columns="id", axis=1, inplace=True)
