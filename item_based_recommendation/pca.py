import numpy as np

# 1. Örnek veri (3 boyutlu)
np.random.seed(42)
X1 = 3 * np.random.randn(200, 1)
X2 = 2 * np.random.randn(200, 1)
X3 = 0.5 * X1 + 0.2 * X2 + np.random.randn(200, 1)
X = np.hstack([X1, X2, X3])   # (200, 3)

# 2. Standardizasyon (manuel)
X_mean = np.mean(X, axis=0)
X_std = np.std(X, axis=0)
Z_score = (X - X_mean)/X_std

# 3. Kovaryans matrisi
cov_matrix = np.cov(Z_score.T)

# 4. Eigen decomposition
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)


# 5. Eigenvalue'lara göre sırala
idx = np.argsort(eigenvalues)[::-1]   # büyükten küçüğe
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

# 6. İlk 2 eigenvector seç (3D -> 2D)
W = eigenvectors[:, :2]   # (3x2)
W.shape
Z_score.shape
# 7. Veri projeksiyonu
X_pca = Z_score @ W   # (200x2)

print("Kovaryans matrisi:\n", cov_matrix)
print("\nEigenvalue'lar:\n", eigenvalues)
print("\nEigenvector'lar:\n", eigenvectors)
print("\nİlk 5 PCA sonucu:\n", X_pca[:5])
