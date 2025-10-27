# Örnek: 4 özellikli bir veri setimiz olsun ve 2 sınıflı bir çıktı bekleyelim.
from func import *
# 1. Ağı oluştur
model = NeuralNetwork()

# 2. Katmanları ekle
#    - İlk katman: 4 girişli, 16 nöronlu, 'relu' aktivasyonlu
#    - İkinci katman: 8 nöronlu, 'relu' aktivasyonlu
#    - Çıkış katmanı: 2 nöronlu (2 sınıf için), 'softmax' aktivasyonlu
model.dense(number_of_neurons=16, activation_function='relu', input_shape=4)
model.dense(number_of_neurons=8, activation_function='relu')
model.dense(number_of_neurons=2, activation_function='softmax')

# 3. Rastgele bir girdi verisi oluşturalım
#    - 5 örnek, 4 özellik (5x4 matris)
sample_data = np.random.randn(5, 4)

# 4. İleri yayılımı çalıştır ve sonucu gör
final_output = model.forward(sample_data)

print("Girdi Verisinin Şekli:", sample_data.shape)
print("Model Çıktısının Şekli:", final_output.shape)
print("\nModel Çıktısı (ilk 5 örnek için olasılıklar):\n", final_output)
