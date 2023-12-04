import matplotlib.pyplot as plt

categories = ['Category 1', 'Category 2', 'Category 3']
values = [15, 23, 8]  # Example values for the number of questions correct
colors = ['#ffb3ba', '#baffc9', '#bae1ff']  # Pastel red, green, and blue

plt.figure(figsize=(8, 6))
plt.bar(categories, values, color=colors)

plt.title('Number of Questions Correct by Category')
plt.ylabel('Number of Questions Correct')
plt.xlabel('Categories')

print(plt.show())
