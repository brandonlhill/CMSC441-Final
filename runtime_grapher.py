import matplotlib.pyplot as plt
import numpy as np

x1, y1 = [], []
with open('allResultsPR.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        x1.append(float(line[0]))
        y1.append(float(line[1]))

x2, y2 = [], []
with open('allResultsTD.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        x2.append(float(line[0]))
        y2.append(float(line[1]))

fig = plt.figure(figsize=(8, 6))

plt.scatter(x1, y1, s=20, color='#15a8ac', label='Pollard\'s rho algorithm') # Plot PR
plt.scatter(x2, y2, s=20, color='#FFA500', label='Trial division') # Plot TD
plt.xlim(1e2, 1e32) # Fix limits of graph
plt.ylim(-10, 125)
plt.xscale('log', base=2) # Base log_2 for x axis
plt.grid(True, linewidth=0.2, color='#DDDDDD')
plt.legend()
plt.xlabel('Semiprime (ℕ)')
plt.ylabel('Time (s)')
plt.subplots_adjust(bottom=0.15)
plt.title('Time to Factor vs Size of Semiprime', loc='center', y=-0.2, fontweight='bold', fontsize=20)




x = np.array(x1)
y = np.array(y1)
coefficients = np.polyfit(np.log2(x), np.log(y), 1) # Fit exponential curve to the data
a, b = np.exp(coefficients[1]), coefficients[0]
plt.plot(x, a * np.exp(b * np.log2(x)), color='red', label='Pollard\'s rho fit')

corr_matrix = np.corrcoef(np.log2(x), np.log(y)) # Calculate R-squared value
r_squared = corr_matrix[0, 1] ** 2

equation_text = f"y = {a:.2e} * exp({b:.2e} * x)"
r_squared_text = f"R² = {r_squared:.2f}"

plt.text(1.5e2, 75, f"Pollard's rho:\n{equation_text}\nR² = {r_squared:.2f}", fontsize=12)




x = np.array(x2)
y = np.array(y2)
