from autoencoder_feeder_lib import WholeGraph as WG

import matplotlib.pyplot as plt
import numpy as np
from make_sets import Source as SS

source_dir = SS()
graph = WG()
BINS = 50

name = "sen_data/inhale/" + "154" +".wav"

matrix = graph.make_matrix_from_name(name)
aa = np.array(matrix)
carrier = np.reshape(aa, [16,50])

numbers = np.linspace(0,15,16)
new_matrix =np.transpose(carrier)
plt.figure(num='INHALE')
for i in range(BINS):
    plt.plot(numbers, new_matrix[i], label = str(i))
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=10, mode="expand", borderaxespad=0.)


name = "sen_data/unknown/" + "120" +".wav"

matrix = graph.make_matrix_from_name(name)
aa = np.array(matrix)
carrier = np.reshape(aa, [16,50])

numbers = np.linspace(0,15,16)
new_matrix =np.transpose(carrier)
plt.figure(num='NOISE')
for i in range(BINS):
    plt.plot(numbers, new_matrix[i], label = str(i))
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=10, mode="expand", borderaxespad=0.)

name = "sen_data/exhale/" + "39" +".wav"


matrix = graph.make_matrix_from_name(name)
aa = np.array(matrix)
carrier = np.reshape(aa, [16,50])

numbers = np.linspace(0,15,16)
new_matrix =np.transpose(carrier)
plt.figure(num='EXHALE')
for i in range(BINS):
    plt.plot(numbers, new_matrix[i], label = str(i))
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=10, mode="expand", borderaxespad=0.)

plt.show()