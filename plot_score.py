import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

results = pd.read_csv(os.path.join('./iteration_score_discount1.csv'))

plt.figure(1)
plt.scatter(results['Episode'], results['Score'], label = 'Score')
plt.plot(results['Episode'], results['MAVG'], label = 'MAVG', color = 'red')
plt.show()
