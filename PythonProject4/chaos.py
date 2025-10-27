import numpy as np
from PIL import Image


WIDTH = 1920
HEIGHT = 1080
NUM_POINTS = 8_000_000


image_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)


vertices = np.array([
    [WIDTH // 2, 50],
    [50, HEIGHT - 50],
    [WIDTH - 50, HEIGHT - 50]
])


colors = np.array([
    [255, 100, 100],
    [100, 255, 100],
    [100, 100, 255]
], dtype=np.uint8)


P = vertices[0].astype(float)

print(f"{WIDTH}x{HEIGHT} tuvalde Kaos Oyunu başlıyor...")
print(f"{NUM_POINTS} adet nokta çizilecek...")

#
for _ in range(20):
    choice = np.random.randint(0, 3)
    P = (P + vertices[choice]) / 2.0

for i in range(NUM_POINTS):
    choice = np.random.randint(0, 3)
    P = (P + vertices[choice]) / 2.0


    x, y = int(P[0]), int(P[1])
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        image_data[y, x] = colors[choice]

print("Fraktal tamamlandı. Görsel kaydediliyor...")

# --- ADIM 4: Kaydetme ---
img = Image.fromarray(image_data, 'RGB')
output_filename = "kaos_oyunu_sierpinski.png"
img.save(output_filename)

print(f"Görsel başarıyla '{output_filename}' olarak kaydedildi.")
# img.show()