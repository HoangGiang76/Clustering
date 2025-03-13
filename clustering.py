import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

conn = mysql.connector.connect(
    host="127.0.0.1",      # Đổi nếu cần
    user="root",           # Đổi nếu có user khác
    password="@Obama123",   # Đổi theo mật khẩu của bạn
    database="sakila"
)

query = """
SELECT 
    c.customer_id,
    SUM(p.amount) AS total_amount_spent,
    COUNT(r.rental_id) AS rental_count
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.customer_id;
"""

df = pd.read_sql(query, conn)
conn.close()

#Chuẩn Hóa Dữ Liệu
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[["total_amount_spent", "rental_count"]])

#Phân Cụm K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(df_scaled)

#Hiển Thị Biểu Đồ
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="rental_count", y="total_amount_spent", hue="cluster", palette="Set1")
plt.title("Phân cụm khách hàng theo mức độ chi tiêu")
plt.xlabel("Số lần thuê phim")
plt.ylabel("Tổng số tiền chi tiêu ($)")
plt.legend(title="Cụm khách hàng")
plt.savefig("scatter_plot.png", dpi=300)
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="cluster", y="total_amount_spent", palette="Set2")
plt.title("So sánh mức chi tiêu giữa các cụm khách hàng")
plt.xlabel("Cụm khách hàng")
plt.ylabel("Tổng tiền chi tiêu ($)")
plt.savefig("boxplot.png", dpi=300)
plt.show()

#Lưu Kết Quả Xuống Excel
df.to_excel("customer_clusters.xlsx", index=False)
print("Dữ liệu đã lưu vào customer_clusters.xlsx")