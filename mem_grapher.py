import matplotlib.pyplot as plt
import numpy as np
x1 = [8,16,32,48,56,58,59,60,61,63,64,70,75,80,85]
y1 = [18.94921875,18.9609375,18.96875,18.97265625,18.984375,18.98828125,18.99609375,19.0,19.0,19.002,19.0078125,19.01171875, 19.01173, 19.015625, 19.01953125]

x2 = [8,16,32,48,56,58,59,60,61,63,64,70]
y2 = [18.6953125,18.70703125,18.7109375,18.71484375,18.7265625,18.75390625,18.765625,18.76953125,18.8046875,18.9140625,19.02734375,20.17578125]
LABEL1 = 'Pollard\'s rho algorithm'
LABEL2 = 'Trial division'
XNAME = 'Size of Semiprime (bits)'
YNAME = 'Memory Usage (Mib)'
fig = plt.figure(figsize=(8, 6))

plt.scatter(x1, y1, s=20, color='#15a8ac', label=LABEL1) # Plot PR
plt.scatter(x2, y2, s=20, color='#FFA500', label=LABEL2) # Plot TD
plt.xlim(1e-1, 1e2) # Fix limits of graph
plt.ylim(15, 21)
plt.xscale('log', base=2) # Base log_2 for x axis
plt.grid(True, linewidth=0.2, color='#DDDDDD')
plt.legend()
plt.xlabel(XNAME)
plt.ylabel(YNAME)
plt.subplots_adjust(bottom=0.15)
plt.title('Memory consumption vs Size of Semiprime', loc='center', y=-0.2, fontweight='bold', fontsize=20)




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
coefficients = np.polyfit(np.log2(x), np.log(y), 1) # Fit exponential curve to the data
a, b = np.exp(coefficients[1]), coefficients[0]
plt.plot(x, a * np.exp(b * np.log2(x)), color='red', label='Trial division fit')

corr_matrix = np.corrcoef(np.log2(x), np.log(y)) # Calculate R-squared value
r_squared = corr_matrix[0, 1] ** 2

equation_text = f"y = {a:.2e} * exp({b:.2e} * x)"
r_squared_text = f"R² = {r_squared:.2f}"

plt.text(1.5e2, 50, f"Trial division:\n{equation_text}\nR² = {r_squared:.2f}", fontsize=12)



plt.savefig('Space_semiprime.png', dpi=300)

print("FINISHED")
print(len(x1))