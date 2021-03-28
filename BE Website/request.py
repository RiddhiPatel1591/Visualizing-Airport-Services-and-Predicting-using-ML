import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'departure_date_time':1/10/2018 10:00:00, 'origin':'ATL', 'destination':'SEA'})

print(r.json())


