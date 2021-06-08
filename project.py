import numpy as np
import pandas as pd

population_data = pd.read_excel(r".\Country Tech Use\country_population_data_by_year.xlsx")
population_data.drop(population_data.columns[1:176], axis=1, inplace=True)
population_data.drop(population_data.columns[46:], axis=1, inplace=True)
print(population_data)

cell_phone_users_data = pd.read_excel(r".\Country Tech Use\total_cell_phones_by_country.xlsx")
internet_users_data = pd.read_excel(r".\Country Tech Use\percentage_population_internet_users.xlsx")

world_tech_data = pd.merge(population_data, cell_phone_users_data, on='country', how='inner')
print(world_tech_data)

world_tech_data.to_excel(r'TestData.xlsx', index=False)

# print(cell_phone_users_data)
# print(internet_users_data)




