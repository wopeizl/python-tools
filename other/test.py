
import numpy as np
LA = np.linalg

# a = np.array([[1, 3, 4], [5, 6, 9], [1, 2, 3], [7, 6, 8]])
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
print(a)
# [[1 3 4]
#  [5 6 9]
#  [1 2 3]
#  [7 6 8]]
U, s, Vh = LA.svd(a, full_matrices=False)
assert np.allclose(a, np.dot(U, np.dot(np.diag(s), Vh)))

print(U)
print(s)
print(Vh)

s[2:] = 0
new_a = np.dot(U, np.dot(np.diag(s), Vh))
print(new_a)