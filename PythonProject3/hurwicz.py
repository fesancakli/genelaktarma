import numpy as np
import matplotlib.pyplot as plt


alpha = np.linspace(0, 1, 500)


h_a1 = 25 - 20 * alpha
h_a2 = 23 - 16 * alpha
h_a3 = 21 - 9 * alpha
h_a4 = 30 - 15 * alpha

plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 8))

plt.plot(alpha, h_a1, label='$H(a_1) = 25 - 20\\alpha$')
plt.plot(alpha, h_a2, label='$H(a_2) = 23 - 16\\alpha$')
plt.plot(alpha, h_a3, label='$H(a_3) = 21 - 9\\alpha$')
plt.plot(alpha, h_a4, label='$H(a_4) = 30 - 15\\alpha$')


en_iyi_karar = np.minimum.reduce([h_a1, h_a2, h_a3, h_a4])
plt.plot(alpha, en_iyi_karar, color='black', linewidth=4, linestyle='-', label='En İyi Karar (Minimum Kayıp)')


kritik_nokta1 = 2/7
kritik_nokta2 = 0.5
plt.axvline(x=kritik_nokta1, color='red', linestyle='--', linewidth=1.5, label=f'Kritik Nokta: α ≈ {kritik_nokta1:.3f}')
plt.axvline(x=kritik_nokta2, color='green', linestyle='--', linewidth=1.5, label=f'Kritik Nokta: α = {kritik_nokta2:.3f}')

plt.title('Hurwicz Kriteri Karar Analizi Grafiği', fontsize=16)
plt.xlabel('İyimserlik Katsayısı (α)', fontsize=12)
plt.ylabel('Beklenen Kayıp Değeri (H)', fontsize=12)
plt.xlim(0, 1)
plt.legend(fontsize=11)


plt.show()