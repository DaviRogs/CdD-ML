import pandas as pd

# Carrega o CSV com os dados de despesas
df1 = pd.read_csv('despesas_deputados_2022.csv', encoding='utf-8-sig')
df2 = pd.read_csv('despesas_deputados_2023.csv', encoding='utf-8-sig')
df3 = pd.read_csv('despesas_deputados_2024.csv', encoding='utf-8-sig')
df4 = pd.read_csv('despesas_deputados_2025.csv', encoding='utf-8-sig')

# Concatenando os DataFrames
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Mediana de cada DataFrame
mediana1 = df1['valor'].median()
mediana2 = df2['valor'].median()
mediana3 = df3['valor'].median()
mediana4 = df4['valor'].median()

# Calculando a mediana geral
mediana = df['valor'].median()

# Calculando a moda de cada DataFrame
moda1 = df1['valor'].mode()[0]  # Pode haver mais de uma moda
moda2 = df2['valor'].mode()[0]  # Pode haver mais de uma moda
moda3 = df3['valor'].mode()[0]  # Pode haver mais de uma moda
moda4 = df4['valor'].mode()[0]  # Pode haver mais de uma moda

moda = df['valor'].mode()  # Pode haver mais de uma moda

print(f"Mediana 2022: R${mediana1:.2f}")
print(f"Mediana 2023: R${mediana2:.2f}")
print(f"Mediana 2024: R${mediana3:.2f}")
print(f"Mediana 2025: R${mediana4:.2f}")
print(f"\nMediana Geral: R${mediana:.2f}\n\n")

print(f"Moda 2022: R${moda1:.2f}")
print(f"Moda 2023: R${moda2:.2f}")
print(f"Moda 2024: R${moda3:.2f}")
print(f"Moda 2025: R${moda4:.2f}")
print(f"\nModa Geral: R${moda[0]:.2f}\n\n")

print("Resumo Estatístico ano 2022:")
print(df1['valor'].describe())
print("\n\n")

print("Resumo Estatístico ano 2023:")
print(df2['valor'].describe())
print("\n\n")

print("Resumo Estatístico ano 2024:")
print(df3['valor'].describe())
print("\n\n")

print("Resumo Estatístico ano 2025:")
print(df4['valor'].describe())
print("\n\n")

print("Resumo Estatístico Geral:")
print(df['valor'].describe())
print("\n\n")