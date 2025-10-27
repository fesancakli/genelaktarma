import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# Logistic map fonksiyonu
def logistic_map(x, r, n):
    seq = []
    for _ in range(n):
        x = r * x * (1 - x)
        seq.append(x)
    return seq

# Mesajı binary string'e çevir
def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

# Binary string'i tekrar text'e çevir
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

# XOR ile şifreleme/çözme
def xor_encrypt(binary, key_stream):
    return ''.join(str(int(b) ^ int(k)) for b, k in zip(binary, key_stream))

# Örnek kullanım
message = "Kaos Güvenlik"
binary_message = text_to_bin(message)

# Logistic map'ten anahtar üret
key_stream = logistic_map(0.7, 3.99, len(binary_message))
key_stream_bin = [str(int(k > 0.5)) for k in key_stream]  # threshold ile binary yap

# Şifreleme
cipher_binary = xor_encrypt(binary_message, key_stream_bin)
cipher_text = bin_to_text(cipher_binary)
print("Şifreli Mesaj:", cipher_text)

# Çözme (aynı key_stream kullanılırsa orijinal gelir)
decrypted_binary = xor_encrypt(cipher_binary, key_stream_bin)
decrypted_text = bin_to_text(decrypted_binary)
print("Çözülen Mesaj:", decrypted_text)
################



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import matplotlib.pyplot as plt

# import matplotlib.animation as animation # Animasyon için artık gerek yok

# Fiziksel sabitler
g = 9.81
L1, L2 = 1.0, 1.0  # uzunluklar
m1, m2 = 1.0, 1.0  # kütleler

# Başlangıç koşulları
theta1, theta2 = np.pi / 2, np.pi / 2 - 1  # açı (radyan)
omega1, omega2 = 0.0, 0.0  # açısal hız
dt = 0.01

# ---- HIZLI TEST İÇİN BU DEĞERLERİ KULLANABİLİRSİNİZ ----
# steps = 500         # Tek simülasyon adımı
# N = 50            # grid çözünürlüğü (50x50)
# ----------------------------------------------------

# ---- TAM ÇÖZÜNÜRLÜK (Yavaş) ----
steps = 500
N = 50  # grid çözünürlüğü (200x200)


# ---------------------------------

# Diferansiyel denklemler
def derivatives(state):
    theta1, omega1, theta2, omega2 = state
    delta = theta2 - theta1

    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta) ** 2
    den2 = (L2 / L1) * den1

    a1 = (m2 * L1 * omega1 ** 2 * np.sin(delta) * np.cos(delta) +
          m2 * g * np.sin(theta2) * np.cos(delta) +
          m2 * L2 * omega2 ** 2 * np.sin(delta) -
          (m1 + m2) * g * np.sin(theta1)) / den1

    a2 = (-m2 * L2 * omega2 ** 2 * np.sin(delta) * np.cos(delta) +
          (m1 + m2) * (g * np.sin(theta1) * np.cos(delta) -
                       L1 * omega1 ** 2 * np.sin(delta) -
                       g * np.sin(theta2))) / den2

    return np.array([omega1, a1, omega2, a2])


# RK4 integratörü
def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)
    k3 = derivatives(state + 0.5 * dt * k2)
    k4 = derivatives(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


# ----- BÖLÜM 1: Tek Simülasyon (Faz Uzayı için) -----
print(f"Bölüm 1: Faz uzayı için tek simülasyon ({steps} adım) çalıştırılıyor...")
state = np.array([theta1, omega1, theta2, omega2])
theta1_list, omega1_list = [], []
# x1_list, y1_list, x2_list, y2_list = [], [], [], [] # Animasyon için artık gerek yok

for _ in range(steps):
    state = rk4_step(state, dt)
    t1, w1, t2, w2 = state
    theta1_list.append(t1)
    omega1_list.append(w1)

    # Animasyon için koordinat hesaplamaları kaldırıldı
    # x1 = L1*np.sin(t1)
    # ... vb.

# ----- BÖLÜM 2: Animasyon (KALDIRILDI) -----
# fig, ax = plt.subplots(figsize=(6,6))
# ... (ilgili tüm animasyon kodları kaldırıldı) ...
# plt.show()

# ----- BÖLÜM 3: Faz Uzayı (theta1 - omega1) -----
print("Faz uzayı grafiği oluşturuluyor...")
plt.figure(figsize=(6, 6))
plt.plot(theta1_list, omega1_list, '.', markersize=0.5, color="blue")
plt.xlabel("Theta1 (açı)")
plt.ylabel("Omega1 (açısal hız)")
plt.title("Double Pendulum Faz Uzayı (RK4)")
plt.show()  # Faz uzayı grafiğini göster

# ----- BÖLÜM 4: Başlangıç Hassasiyet Haritası (YAVAŞ KISIM) -----
print(f"Bölüm 4: {N}x{N} hassasiyet haritası oluşturuluyor... (Bu işlem uzun sürebilir!)")

# Başlangıç gridini oluştur
theta1_vals = np.linspace(-np.pi, np.pi, N)
theta2_vals = np.linspace(-np.pi, np.pi, N)
image = np.zeros((N, N))

# Her başlangıç için simülasyon
for i, t1 in enumerate(theta1_vals):
    # İlerleme durumunu görmek için basit bir sayaç
    if i % (N // 10) == 0:
        print(f"Harita ilerlemesi: {int(100.0 * i / N)}%")

    for j, t2 in enumerate(theta2_vals):
        state = np.array([t1, 0.0, t2, 0.0])  # açılar, hızlar sıfır
        for _ in range(steps):
            state = rk4_step(state, dt)
        # son durumda ikinci açının yönüne göre renklendir
        image[j, i] = np.sin(state[2])  # θ2'nin sinüsü işaret verir

print("Harita hesaplaması bitti. Görselleştiriliyor...")

# ----- BÖLÜM 5: Görselleştirme (Renk Değiştirildi) -----
plt.figure(figsize=(8, 8))

# cmap='seismic' yerine 'viridis' kullanıldı
# Diğer güzel seçenekler: 'plasma', 'inferno', 'magma', 'gnuplot'
plt.imshow(image, extent=[-np.pi, np.pi, -np.pi, np.pi], origin='lower', cmap='viridis')

plt.colorbar(label="Son durumda sin(θ2)")
plt.xlabel("θ1 (radyan)")
plt.ylabel("θ2 (radyan)")
plt.title("Double Pendulum Başlangıç Hassasiyet Haritası")
plt.show()  # Son haritayı göster

print("İşlem tamamlandı.")