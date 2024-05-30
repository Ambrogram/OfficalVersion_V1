import matplotlib.pyplot as plt

def test_plot():
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('Test Plot')
    plt.show()

test_plot()
