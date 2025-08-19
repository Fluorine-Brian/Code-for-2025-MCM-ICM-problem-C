import pandas as pd
import numpy as np

# 读取数据集
data = pd.read_csv('summerOly_programs.csv', encoding='latin1')

# 1. 查看数据的所有列名，找出实际存在的年份列
print("所有列名：")
print(data.columns)

# 2. 确保年份列的范围正确，例如 1896, 1900, ..., 2024（不包含不存在的年份）
year_columns = [str(year) for year in range(1896, 2025, 4)]  # 每隔4年的年份列
# 手动添加特殊的年份列如 '1906*'，以便后续处理
year_columns.append('1906*')  # 添加特殊列

# 检查数据集中哪些年份列存在
valid_year_columns = [year for year in year_columns if year in data.columns]
print("\n有效的年份列：")
print(valid_year_columns)

# 3. 将有效的年份列转换为数值类型
for year in valid_year_columns:
    data[year] = pd.to_numeric(data[year], errors='coerce')

# 4. 处理其他可能的文本列，避免 Categorical 错误
# 将 Categorical 列转换为字符串类型，以便 fillna 可以工作
data['Discipline'] = data['Discipline'].astype(str)
data['Code'] = data['Code'].astype(str)
data['Sport'] = data['Sport'].astype(str)

# 5. 处理数据中的空值（NaN），将所有空值填充为0
data.fillna(0, inplace=True)

# 6. 查看数据类型检查
print("\n数据类型检查：")
print(data.dtypes)

# 7. 查看数据处理后的前几行
print("\n数据处理后的预览：")
print(data.head())


# 8. 如果需要将清理后的数据保存为新的文件
data.to_csv('summerOly_hosts_processed.csv', index=False)
