import numpy as np

# Create a 2D numpy array
matrix_1 = np.array([[1, 2], [3, 4]])

# Create a 2D numpy array
matrix_2 = np.array([[5, 6], [7, 8]])

# Print the array
print("Matrix 1:")
for i in matrix_1:
    print(i[0], i[1])

print("Matrix 2:")
for i in matrix_2:
    print(i[0], i[1])

# Add the two matrices
result = np.add(matrix_1, matrix_2)

# Print the result
print("Sum:")
for i in result:
    print(i[0], i[1])

# Subtract the two matrices
result = np.subtract(matrix_1, matrix_2)

# Print the result
print("Subtract:")
for i in result:
    print(i[0], i[1])

# Multiply the two matrices
result = np.multiply(matrix_1, matrix_2)

# Print the result
print("Multiplication:")
for i in result:
    print(i[0], i[1])

# Divide the two matrices
result = np.divide(matrix_1, matrix_2)

# Print the result
print("Deviation:")
for i in result:
    print(i[0], i[1])

# Calculate the dot product of the two matrices
result = np.dot(matrix_1, matrix_2)

# Print the result
print("Product:")
for i in result:
    print(i[0], i[1])

# Calculate the inverse of the matrix_1
result = np.linalg.inv(matrix_1)

# Print the result
print("Inverse:")
for i in result:
    print(i[0], i[1])

# Calculate the transpose of the matrix_1
result = np.transpose(matrix_1)

# Print the result
print("Transpose:")
for i in result:
    print(i[0], i[1])

# Calculate the trace of the matrix_1
trace = np.trace(matrix_1)

# Print the result
print(trace)


# Calculate the determinant of the matrix_1
determinant = np.linalg.det(matrix_1)
print("Determinant: ", determinant)


