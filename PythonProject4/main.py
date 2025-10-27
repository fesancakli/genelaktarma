import numpy as np
from PIL import Image
import sys


IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080


NUM_STEPS = 10_000_000
DIMENSIONS = 5

np.set_printoptions(threshold=sys.maxsize)

print(f"{IMAGE_WIDTH}x{IMAGE_HEIGHT} boyutunda {NUM_STEPS} adımlık 5D yürüyüş oluşturuluyor...")


dims_to_move = np.random.randint(0, DIMENSIONS, size=NUM_STEPS)
steps = np.random.choice([-1, 1], size=NUM_STEPS)
delta = np.zeros((NUM_STEPS, DIMENSIONS), dtype=int)
delta[np.arange(NUM_STEPS), dims_to_move] = steps
walk = np.cumsum(delta, axis=0)
del delta

print("Yürüyüş verisi oluşturuldu. Piksellere haritalanıyor...")

x = walk[:, 0]
y = walk[:, 1]
x_range = x.max() - x.min()
y_range = y.max() - y.min()
scale_x = IMAGE_WIDTH / (x_range + 1e-6)
scale_y = IMAGE_HEIGHT / (y_range + 1e-6)
scale = min(scale_x, scale_y)
x_scaled = ((x - x.min()) * scale).astype(int)
y_scaled = ((y - y.min()) * scale).astype(int)


a = 50
b = 130
H = ((walk[:, 2] % b) + a).astype(np.uint8)


S = ((walk[:, 3] % 106) + b).astype(np.uint8)
V = ((walk[:, 4] % 106) + b).astype(np.uint8)

del walk


hsv_data = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)

hsv_stack = np.stack([H, S, V], axis=1)
hsv_data[y_scaled, x_scaled] = hsv_stack
img_hsv = Image.fromarray(hsv_data, 'HSV')
img_rgb = img_hsv.convert('RGB')


output_filename = "gorselim.png"
img_rgb.save(output_filename)

print(f"Görsel başarıyla '{output_filename}' olarak kaydedildi.")
# img_rgb.show()