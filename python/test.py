import json
import pandas as pd

def get_json_data(fname: str) -> list:
	json_data = []
	with open('cadets.json', 'r') as f:
		for line in f:
			json_data.append(json.loads(line))
	return (json_data)

def make_data(json_list: list) -> pd.DataFrame:
	data = {"Name": [], "Full_Name": [], "Level": [],
			"batch_month": [], "batch_year": [], 
			"blackhole_date": []}#, "days_before_blackhole": []}
	for i in range(0, len(json_list[0])):
		data["Name"].append(json_list[0][i]["login"])
		data["Full_Name"].append(json_list[0][i]["displayname"])
		data["batch_month"].append(json_list[0][i]["pool_month"])
		data["batch_year"].append(json_list[0][i]["pool_year"])
		data["Level"].append(json_list[0][i]["cursus_users"][1]["level"])
		data["blackhole_date"].append(json_list[0][i]["cursus_users"][1]["blackholed_at"])
	return (pd.DataFrame(data))

if __name__ == "__main__":
	name = "cadets.json"
	try:
		data = get_json_data(name)
		df = make_data(data)
		df.to_csv("output.csv")
	except Exception as error:
		print("Error occured:" + str(error))