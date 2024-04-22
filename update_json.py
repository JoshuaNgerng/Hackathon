import json
import requests

class get_42_api:
	def __init__(self, UID, SECRET) -> None:
		__doc__ = '''
		Init the neccessary components to make url request
		all info received from 42 is in form of json
		get all user login name first
		then make request and filter every person in 42kl
		the final output would be four json files for another script to process
		'''
		self.UID = UID
		self.SECRET = SECRET
		self.headers = {'Content-type':'application/json'}
		self.connect = requests.post(f"https://api.intra.42.fr/oauth/token?grant_type=client_credentials&client_id={UID}&client_secret={SECRET}", 
							   		headers=self.headers)
		if (self.connect.status_code != requests.codes.ok):
			raise Exception("request failed")
		self.token = self.connect.json()['access_token']
		self.names = None
	
	def get_name_list(self):
		__doc__ = ''''
		get 100 users from KL campus at a time
		ends when the request return less than 100 users
		outputs the login name of all users
		'''
		i = 1
		tol = 100
		full_list = []
		while tol == 100:
			url = f"https://api.intra.42.fr/v2/campus/34/users?per_page=100&page={i}&access_token={self.token}"
			response = requests.get(url)
			full_list += response.json()
			tol = len(response.json())
			i += 1
		out = []
		for i in range(0, len(full_list)):
			out.append(full_list[i]["login"])
		return (out)

	def get_all_user_info(self, names: list = None) -> None:
		__doc__ = ''''
		sort through every name in name list
		find active users into sort into follow groups
		0 -> staff
		1 -> cadet
		2 -> psciners
		'''
		if (names is None):
			names = self.names
		if (names is None):
			return (None)
		staffs = []
		cadets = []
		psc = []
		unkn = []
		for user in names:
			response = requests.get(f'https://api.intra.42.fr/v2/users/{user}?access_token={self.token}')
			j = response.json()
			if (j['staff?'] == True):
				staffs.append(j)
			elif (len(j['cursus_users']) > 1 and j['cursus_users'][1]['grade'] in ["Member","Learner"]):
				cadets.append(j)
			elif (len(j['cursus_users']) == 1 and j['cursus_users'][0]['grade']):
				psc.append(j)
			else:
				unkn.append(j)
		with open("cadets.json", "w") as f:
			f.write(json.dumps(cadets))
		with open("staffs.json", "w") as f:
			f.write(json.dumps(staffs))
		with open("psciners.json", "w") as f:
			f.write(json.dumps(psc))
		with open("unclassify.json", "w") as f:
			f.write(json.dumps(unkn))		

if __name__ == "__main__":
	UID = "u-s4t2ud-93f98ed7322b2315f21182fb993d3b7c12368e20e03e6c73359ebced64b8ec31"
	SECRET = "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"
	UPDATE = get_42_api(UID, SECRET)
	# UPDATE.names = UPDATE.get_name_list()
	# UPDATE.get_all_user_info(UPDATE.names)
