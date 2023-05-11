import numpy as np
import matplotlib.pyplot as plt


# Check number of samples
def checkNumOfSamples(*samples):
    for i in range(1, len(samples)):
        if len(samples[i - 1]) != len(samples[i]):
            print(
                "sample " + str(i - 1) + " and " + str(i) + " are not the same length"
            )
            return False
        print("samples have the same length")
        return True


# plot number of samples
def plotSamples(**samples):
    # Figuring out the number of subplots
    numSamples = len(samples.keys())
    N = (numSamples / 2) if (numSamples % 2 == 0) else (math.floor(numSamples / 2) + 1)

    fig, axs = plt.subplots(N, 2)
    fig.suptitle("Plot of the Waves (1 Period)")

    i = 0
    j = 0

    for name, sample in samples.items():
        if j == 2:
            j = 0
            i += 1
        axs[i, j].plot(sample)
        axs[i, j].set_title(name)
        j += 1
    fig.tight_layout()


# find best combination
def find_ab(mat_a, mat_b, mat_result):
    diff_min = float("inf")
    a_opt = 0
    b_opt = 0

    for a in np.arange(0, 1, 0.01):
        b = 1 - abs
        comb_mat = a * mat_a + b * mat_b
        diff = np.sum(np.abs(comb_mat - mat_result))

        if diff < diff_min:
            diff_min = diff
            a_opt = a
            b_opt = b
    return a_opt, b_opt
