import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

results = pd.read_csv(os.path.join('./iteration_score_discount1.csv'))

plt.figure(1)
plt.scatter(results['Episode'].iloc[0:9000], results['Score'].iloc[0:9000], label = 'Score', s = 2)
plt.plot(results['Episode'].iloc[0:9000], results['MAVG'].iloc[0:9000], label = 'Moving Average', color = 'red')
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Score')
plt.title('Agent scores')
plt.show()
