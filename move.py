import json
import matplotlib.pyplot as plt
import numpy as np

_2 = json.load(open('/Users/tyt15771/Documents/VS_ECFP/LTSR_2.json', 'r'))
_3 = json.load(open('/Users/tyt15771/Documents/VS_ECFP/LTSR_3.json', 'r'))
_4 = json.load(open('/Users/tyt15771/Documents/VS_ECFP/LTSR_4.json', 'r'))
_5 = json.load(open('/Users/tyt15771/Documents/VS_ECFP/LTSR_5.json', 'r'))
_7 = json.load(open('/Users/tyt15771/Documents/VS_ECFP/LTSR_7.json', 'r'))
_9 = json.load(open('/Users/tyt15771/Documents/VS_ECFP/LTSR_9.json', 'r'))

plt.scatter([2]*len(_2), _2)
plt.scatter([3]*len(_3), _3)
plt.scatter([4]*len(_4), _4)
plt.scatter([5]*len(_5), _5)
plt.scatter([7]*len(_7), _7)
plt.scatter([9]*len(_9), _9)
plt.show()

plt.boxplot([[], _2, _3, _4, _5, [], _7, [], _9])
plt.ylim(-0.05, 1.05)
plt.yticks(np.arange(0.0, 1.1, 0.1))
plt.xlabel('radius of sample patch')
plt.ylabel('tversky similarity')
plt.show()