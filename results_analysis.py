import json
import pandas as pd


def list_to_unique_list(list_: list) -> list:
    return list(dict.fromkeys(list_))


def clear_county(name: str) -> str:
    for i in ["D", "R", "Total"]:
        name = name.replace(i, "")
    return name.strip()


with open(r"results.json") as file:
    data = json.load(file)
counties = list_to_unique_list([clear_county(i) for i in data.keys()])
percentages = []
for county in counties:
     d = round(data[f"{county} D"]/data[f"{county} Total"]*100, 2)
     r = round(data[f"{county} R"]/data[f"{county} Total"]*100, 2)
     percentages += [[d, r]]
df = pd.DataFrame(percentages, index=counties, columns=["D", "R"])
print(df)
     
     