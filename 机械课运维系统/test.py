import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib.font_manager import FontProperties

def main():
    # Set the font properties for Chinese characters
    font_path = '/System/Library/Fonts/STHeiti Light.ttc'  # Path to a font that supports Chinese
    font_prop = FontProperties(fname=font_path)

mu = 1000  # 均值
sigma = 10  # 标准差
x = np.linspace(960, 1040, 100)
y = stats.norm.pdf(x, mu, sigma)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='正态分布曲线')
plt.fill_between(x, y, where=(x >= 970) & (x <= 1030), alpha=0.3, label='±3σ 范围')
plt.axvline(mu, color='r', linestyle='--', label='均值 μ=1000 Å')
    plt.title('晶圆膜厚正态分布 (μ=1000 Å, σ=10 Å)', fontproperties=font_prop)
    plt.xlabel('膜厚 (Å)', fontproperties=font_prop)
    plt.ylabel('概率密度', fontproperties=font_prop)
    plt.legend(prop=font_prop)
plt.grid()
plt.show()

if __name__ == "__main__":
    main()