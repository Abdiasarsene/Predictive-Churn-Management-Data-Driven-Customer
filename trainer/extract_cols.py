from trainer.config import settings
import pandas as pd


data = pd.read_excel(settings.train_dataset)
data.columns