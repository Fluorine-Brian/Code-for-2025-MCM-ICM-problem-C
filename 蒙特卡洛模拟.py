import pandas as pd
import numpy as np
import statsmodels.api as sm
# from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. 数据加载
athletes = pd.read_csv("C://2024 美赛培训-写作指导与发布模板/2025_MCM/code/summerOly_athletes.csv")
medals = pd.read_csv('C://2024 美赛培训-写作指导与发布模板/2025_MCM/code/summerOly_medal_counts.csv')
programs = pd.read_csv('C://2024 美赛培训-写作指导与发布模板/2025_MCM/code/summerOly_programs_processed.csv')

# 2. 数据预处理
# 提取运动员和奖牌数据，按年份和国家进行汇总
athletes['Year'] = pd.to_datetime(athletes['Year'], format='%Y').dt.year
medals_summary = medals.groupby(['NOC', 'Year'])[['Gold', 'Silver', 'Bronze']].sum()

# 创建“优秀教练”变量：可以是一个二元变量，1表示有优秀教练，0表示没有
# 假设优秀教练的数据已经通过某种方式标注在 athletes 中
athletes['GreatCoach'] = athletes['Name'].apply(lambda x: 1 if x in ['Lang Ping', 'Béla Károlyi'] else 0)

# 3. 回归分析模型
# 将教练效应变量（GreatCoach）与奖牌数量（Gold）进行回归分析
X = athletes.groupby(['NOC', 'Year'])['GreatCoach'].sum().reset_index()
y = medals_summary['Gold'].reset_index()

# 合并数据，准备回归分析
data = pd.merge(X, y, on=['NOC', 'Year'], how='inner')

# 检查数据行数
print(data.shape)  # 查看数据行数是否足够

# 检查是否有空值
print(data.isnull().sum())  # 查看是否有缺失值

# 如果数据行数足够，进行回归分析
if len(data) > 1:
    X = data[['GreatCoach']]  # 自变量
    y = data['Gold']  # 因变量
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())
else:
    print("数据不足以进行回归分析。")

# 定义自变量和因变量
X = data[['GreatCoach']]  # 其他自变量可以继续添加
y = data['Gold']

# 添加常数项
X = sm.add_constant(X)

# 进行回归分析
model = sm.OLS(y, X).fit()

# 输出回归分析结果
print(model.summary())

# 4. 预测与模拟
# 使用训练好的回归模型预测未来奥运会奖牌数
future_years = np.array([2028])  # 假设预测2028年
future_data = pd.DataFrame({'GreatCoach': [1], 'const': [1]})
predictions = model.predict(future_data)

print("2028年预测金牌数量:", predictions)

# 5. 模拟不同情景下的奖牌数变化（蒙特卡洛方法）
# 假设不同教练更换概率，我们可以模拟教练更换对金牌数量的影响
num_simulations = 1000
simulated_results = []

for _ in range(num_simulations):
    # 随机选择是否有优秀教练
    coach_effect = np.random.choice([0, 1], p=[0.5, 0.5])  # 50%几率
    simulated_results.append(model.predict([1, coach_effect])[0])

# 可视化模拟结果
plt.hist(simulated_results, bins=30, edgecolor='black')
plt.title('Simulated Gold Medal Predictions for 2028')
plt.xlabel('Predicted Gold Medals')
plt.ylabel('Frequency')
plt.show()
