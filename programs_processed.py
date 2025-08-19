import numpy as np
import pandas as pd

programs_data = pd.read_csv("C://2024 美赛培训-写作指导与发布模板/2025_MCM/code/summerOly_programs_processed.csv")

# 检查数据的前几行，确认数据格式
print(programs_data.head())

# 根据 'Sport' 列对每种运动的项目数量进行汇总
# 计算每个运动（如 'Aquatics'）下所有项目的总数
df_sport_summary = programs_data.groupby('Sport').sum(numeric_only=True).reset_index()

# 输出每个运动的项目总数
print(df_sport_summary[['Sport', '2024']])

df_cleaned = df_sport_summary[df_sport_summary['2024'] != 0]


# 将汇总后的数据保存为新的 CSV 文件
output_file = 'summerOly_programs_processed2.csv'  # 你可以选择文件的保存路径
df_cleaned.to_csv(output_file, index=False)

print(f"处理后的文件已保存为: {output_file}")
