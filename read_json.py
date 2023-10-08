import json
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt

class json_to_dataframe:
	def __init__(self) -> None:
		__doc__ = '''
		the information is stored in four json
		each group would have their own dataframe function
		this version can only get the blackhole status of cadets
		'''
		self.cadets = "cadets.json"
		self.staffs = "staffs.json"
		self.psci = "psciners.json"
		self.unkn = "unclassify.json"
		self.json_data = None

	def get_json_data(self, fname: str) -> list:
		__doc__ = '''
		Make a list containing all the json data from a file
		'''
		json_data = []
		with open(fname, 'r') as f:
			for line in f:
				json_data += json.loads(line)
		return (json_data)

	def str_date(self, s: str) -> datetime:
		__doc__ = '''
		use to change str type to proper datetime type
		it truncates the str to have year-month-day only
		'''
		if (s == None):
			return (None)
		format = "%Y-%m-%d"
		s = s[0: 10]
		return (datetime.strptime(s, format))

	def cadet_dataframe(self, now : datetime) -> pd.DataFrame:
		__doc__ = '''
		Make a dataframe by pulling the right in information from json
		Date is a str type that needs to be change
		Status is determine by their member status and the blackhole days
		'''
		if (self.json_data is None):
			print("Have not receive any json file")
			return (None)
		data = {"Name": [], "Full_Name": [], "Level": [],
				"batch_month": [], "batch_year": [], 
				"blackhole_date": [], "days_before_blackhole": [], 
				"status": []}
		for i in range(0, len(self.json_data)):
			data["Name"].append(self.json_data[i]["login"])
			data["Full_Name"].append(self.json_data[i]["displayname"])
			data["batch_month"].append(self.json_data[i]["pool_month"])
			data["batch_year"].append(self.json_data[i]["pool_year"])
			data["Level"].append(self.json_data[i]["cursus_users"][1]["level"])
			t = self.str_date(self.json_data[i]["cursus_users"][1]["blackholed_at"])
			if (t):
				diff = (t - now).days
			else:
				diff = None
			data["blackhole_date"].append(t)
			data["days_before_blackhole"].append(diff)
			grade = self.json_data[i]['cursus_users'][1]['grade']
			if (diff is None and grade in ["Member", "Learner"]):
				data["status"].append("Specialisation")
			elif (diff < 0): # and grade not in ["Member", "Learner"]):
				data["status"].append("Dropped out")
			elif (diff > 0 and grade in ["Member", "Learner"]):
				data["status"].append("In Core")
			else:
				data["status"].append("Unknown")
		return (pd.DataFrame(data))

class dateframe_to_graphs:
	def __init__(self, df: pd.DataFrame) -> None:
		__doc__ = '''
		converts a dataframe to graph
		have functions to filter the df
		can make barplot and pieplot
		'''
		self.df = df
		self.new_df = df
	
	def filter_df_range(self, key_word: str, min: int, max: int, assign: int = 0) -> pd.DataFrame:
		if (key_word is None):
			return (self.new_df)
		if (min is None and max is None):
			return (self.new_df)
		if (min is not None and max is not None):
			q = f"{key_word} >= {min} and {key_word} < {max}"
		elif (min is None and max is not None):
			q = f"{key_word} < {max}"
		else:
			q = f"{key_word} >= {min}"
		if (assign):
			self.new_df = self.new_df.query(q)
			return (self.new_df)
		return (self.new_df.query(q))

	def filter_df_find(self, key_word: str, item: str, assign: int = 0) -> pd.DataFrame:
		if  (key_word is None):
			return (self.new_df)
		if (item is None):
			return (self.new_df)
		if (assign):
			self.new_df = self.new_df.query(f"{key_word} == '{item}'")
			return (self.new_df)
		return (self.new_df.query(f"{key_word} == '{item}'"))

	def make_bar_chart(self, target: str, min: int = None, max: int = None, inc: int = 10):
		if (min is None):
			min = 0
		if (max is None):
			max = self.new_df[target].max()
		bins = [num for num in range(min, max, inc)]
		plt.hist(self.new_df[target], bins=bins, color="lightblue", edgecolor='black')

	def sum_list(self, l: list) -> int:
		out = 0
		for num in l:
			out += int(num)
		return (out)

	def make_pie_chart(self, target: str, min: int = None, max: int = None, inc: int = 10, end: int = 1, my_labels: list = []):
		if (min is None):
			min = 0
		if (max is None):
			max = self.new_df[target].max()
		max_freq = self.new_df[target].max()
		mmax = self.new_df[target].count()
		# print(mmax)
		bins = [num for num in range(min, max, inc)]
		# print(bins)
		# print(self.df)
		val = [self.filter_df_range(target, bins[i], bins[i + 1])[target].count() for i in range(0, len(bins) - 1)]
		if (end == 1 and max != max_freq):
			val.append(int(max_freq) - self.sum_list(val))
		# print(self.df)
		# print(val)
		if (not my_labels):
			my_labels = ["" for v in val]
		i = 0
		for v in val:
			percentage = v/mmax * 100
			# print(percentage)
			s = "{:.1f}".format(percentage)
			my_labels[i] += ": " + s + "%"
			i += 1
		plt.pie(val, labels=my_labels, wedgeprops = {"edgecolor" : "black", 'linewidth': 2, 'antialiased': True})
		plt.savefig('pie.png', bbox_inches='tight')

	def reset_df(self):
		self.new_df = self.df


if __name__ == "__main__":
	# try:
	j2df = json_to_dataframe()
	j2df.json_data = j2df.get_json_data(j2df.cadets)
	df = j2df.cadet_dataframe(datetime.now())
	graph1 = dateframe_to_graphs(df)
	# print(graph1.df)
	graph1.filter_df_find("batch_month", "march", 1)
	# graph1.filter_df_find("batch_year", "2022", 1)
	print(graph1.new_df)
	graph1.make_pie_chart('days_before_blackhole', 0, 30, 7, 0, my_labels= ["one_week", "two_week", "three_week", "four_week"])

	# except Exception as error:
		# print("Error occured:" + str(error))