import pandas as pd

# Leitura do arquivo CSV
df_csv = pd.DataFrame(pd.read_csv('US_Regional_Sales_Data.csv'))

# Converter colunas de datas
date_columns = ['ProcuredDate', 'OrderDate', 'ShipDate', 'DeliveryDate']
for col in date_columns:
    df_csv[col] = pd.to_datetime(
        df_csv[col], format='%d/%m/%Y', errors='coerce')

# Limpar as colunas monetárias e de desconto
df_csv['Unit Cost'] = df_csv['Unit Cost'].replace(
    {r'\$': '', ',': ''}, regex=True).astype(float)
df_csv['Unit Price'] = df_csv['Unit Price'].replace(
    {r'\$': '', ',': ''}, regex=True).astype(float)
df_csv['Discount Applied'] = df_csv['Discount Applied'].astype(float)

# 1 - Função para classificar vendas


def classificar_vendas(qtd):
    if qtd >= 7:
        return 'Diamond'
    elif 5 <= qtd < 7:
        return 'Gold'
    elif 3 <= qtd < 5:
        return 'Silver'
    else:
        return 'Regular'


# Criar a coluna 'Sale Classification'
df_csv['Sale Classification'] = df_csv['Order Quantity'].apply(
    classificar_vendas)

# 2 - Filtrar pedidos 'Diamond'
diamond_orders = df_csv[df_csv['Sale Classification'] == 'Diamond']
print("Pedidos 'Diamond':", diamond_orders)

# 3 - Calcular média de pedidos
media_pedidos = round(df_csv['Order Quantity'].mean(), 2)
print(f'\nA média de pedidos é: {media_pedidos}')

# 4 - Calcular total de vendas no canal 'In-Store'
in_store_sales = df_csv[df_csv['Sales Channel'] == 'In-Store'].copy()
in_store_sales['Total Sales'] = (in_store_sales['Unit Price'] * in_store_sales['Order Quantity']) - \
    (in_store_sales['Discount Applied'] *
     in_store_sales['Unit Price'] * in_store_sales['Order Quantity'])
total_in_store_sales = in_store_sales['Total Sales'].sum()
print(f'\nTotal de vendas no canal "In-Store": ${total_in_store_sales:.2f}')

# 5 - Canal com maior lucro
df_csv['Total Sales'] = (df_csv['Unit Price'] * df_csv['Order Quantity']) - \
    (df_csv['Discount Applied'] *
     df_csv['Unit Price'] * df_csv['Order Quantity'])
sales_channel_totals = df_csv.groupby('Sales Channel')['Total Sales'].sum()
maior_lucro_canal = sales_channel_totals.idxmax()
maior_lucro_valor = sales_channel_totals.max()
print(f'\nO canal de vendas com o maior lucro é: {
      maior_lucro_canal} com um total de vendas de ${maior_lucro_valor:.2f}')

# 6 - Canal com menor lucro
menor_lucro_canal = sales_channel_totals.idxmin()
menor_lucro_valor = sales_channel_totals.min()
print(f'\nO canal de vendas com o menor lucro é: {
      menor_lucro_canal} com um total de vendas de ${menor_lucro_valor:.2f}')

# 7 - Média de lucro do canal 'In-Store' antes de 2019
in_store_pre_2019 = df_csv[(
    df_csv['Sales Channel'] == 'In-Store') & (df_csv['OrderDate'] <= '2018-12-31')]
media_lucro_in_store_pre_2019 = round(
    in_store_pre_2019['Total Sales'].mean(), 2)
print(f'\nA média do lucro do canal "In-Store" em pedidos feitos até 31/12/2018 é: ${
      media_lucro_in_store_pre_2019:.2f}')

# 8 - Média de lucro do canal 'Online' em 2020
online_orders = df_csv[df_csv['Sales Channel'] == 'Online']
online_orders_2020 = online_orders[online_orders['OrderDate'].dt.year == 2020]
if not online_orders_2020.empty:
    media_lucro_online_2020 = round(
        online_orders_2020['Total Sales'].mean(), 2)
else:
    media_lucro_online_2020 = 0
print(f'\nA média do lucro do canal "Online" em pedidos feitos em 2020 é: ${
      media_lucro_online_2020:.2f}')

# 9 - Média de lucro do canal 'Wholesale' antes de 2020
wholesale_orders_pre_2020 = df_csv[(df_csv['Sales Channel'] == 'Wholesale') & (
    df_csv['OrderDate'] <= '2019-12-31')]
media_lucro_wholesale_pre_2020 = round(
    wholesale_orders_pre_2020['Total Sales'].mean(), 2)
print(f'\nA média do lucro do canal "Wholesale" em pedidos feitos até 31/12/2019 é: ${
      media_lucro_wholesale_pre_2020:.2f}')

# 10 - Média de lucro do canal 'Distributor' entre 2019 e 2020
distributor_orders_2019_2020 = df_csv[(df_csv['Sales Channel'] == 'Distributor') &
                                      (df_csv['OrderDate'] >= '2019-01-01') &
                                      (df_csv['OrderDate'] <= '2020-12-31')]
media_lucro_distributor_2019_2020 = round(
    distributor_orders_2019_2020['Total Sales'].mean(), 2)
print(f'\nA média do lucro do canal "Distributor" em pedidos feitos entre 01/01/2019 e 31/12/2020 é: ${
      media_lucro_distributor_2019_2020:.2f}')
