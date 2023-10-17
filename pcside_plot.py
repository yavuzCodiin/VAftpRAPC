import matplotlib.pyplot as plt

# Set up the plot
fig, ax = plt.subplots()

# Define the factor-price ratio and good-price ratio for Country A
factor_price_ratio_A = [1, 1.5, 2]
good_price_ratio_A = [1, 0.8, 0.6]

# Define the factor-price ratio and good-price ratio for Country B
factor_price_ratio_B = [1, 1.5, 2]
good_price_ratio_B = [0.6, 0.8, 1]

# Plot the Heckscher-Ohlin relationship for Country A
ax.plot(factor_price_ratio_A, good_price_ratio_A, color='red', label='Country A')

# Plot the Heckscher-Ohlin relationship for Country B
ax.plot(factor_price_ratio_B, good_price_ratio_B, color='blue', label='Country B')

# Add a legend
ax.legend()

# Add axis labels
ax.set_xlabel('Factor-price ratio (w/r)')
ax.set_ylabel('Good-price ratio (PX/PY)')

# Show the plot

plt.show()