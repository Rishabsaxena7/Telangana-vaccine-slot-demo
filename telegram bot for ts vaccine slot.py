import requests
from datetime import datetime

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot<Bot token>/sendMessage?chat_id=@__groupid__&text="
group_id = "<telegram groupid>"
telangana_district_ids = [581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613]

def fetch_data_from_cowin(district_id):
	query_params = "?district_id={}&date={}".format(district_id, today_date)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	final_url = base_cowin_url+query_params
	response = requests.get(final_url, headers=headers)
	extract_availability_data(response)
	# print(response.text)


def fetch_data_for_state(district_ids):
	for district_id in district_ids:
		fetch_data_from_cowin(district_id)

def extract_availability_data(response):
	response_json = response.json()
	for center in response_json["centers"]:
		for session in center["sessions"]:
				if session["available_capacity"]>0:
					message = "Pincode: {}\n Name: {}\n State: {}\n District: {}\n Fee Type: {}\n Date: {}\n Available Capacity: {}\n Vaccine: {}\n Slots: {}\n Available Capacity Dose1: {}\n Available Capacity Dose2: {}\n Minimum Age: {}".format(
					         center["pincode"], center["name"],center["state_name"],center["district_name"],center["fee_type"],
					         session["date"],session["available_capacity"],session["vaccine"],session["slots"],session["available_capacity_dose1"],session["available_capacity_dose2"],
					         session["min_age_limit"])
					send_message_telegram(message)

def send_message_telegram(message):
	final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
	final_telegram_url = final_telegram_url + message
	response = requests.get(final_telegram_url)
	print(response)


if __name__ == "__main__":
	fetch_data_for_state(telangana_district_ids)

