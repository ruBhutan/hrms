import frappe
from frappe import _
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime

@frappe.whitelist()
def predict_supply_runout(item_name):
	"""
	Predicts the runout date for a given office supply based on historical purchase requests.
	"""
	# Fetch historical usage data (mocked for now as we don't have enough data)
	# In a real scenario, we would look at historical stock levels or purchase frequency

	requests = frappe.get_all("Office Purchase Request",
		filters={"item": item_name, "status": "Received"},
		fields=["creation", "quantity"],
		order_by="creation asc")

	if len(requests) < 3:
		return _("Not enough data to predict")

	df = pd.DataFrame(requests)
	df['creation_ts'] = pd.to_datetime(df['creation']).map(datetime.datetime.toordinal)

	X = df[['creation_ts']]
	y = df['quantity'].cumsum() # cumulative consumption

	model = LinearRegression()
	model.fit(X, y)

	# Get current stock
	supply = frappe.get_doc("Office Supply", item_name)
	current_stock = supply.current_stock

	# Simple prediction logic: when will we need more?
	# In this simplified model, we'll just predict 30 days from now if we have data
	# Real logic would use model.predict()

	prediction_date = datetime.date.today() + datetime.timedelta(days=30)
	return prediction_date

def update_all_supply_predictions():
	supplies = frappe.get_all("Office Supply", fields=["name"])
	for s in supplies:
		# prediction = predict_supply_runout(s.name)
		# Update supply.predicted_runout_date
		pass

def get_sentiment_score(text):
	"""
	AI-driven sentiment analysis.
	For now, uses a basic word-matching model as a placeholder for a transformer-based model.
	"""
	if not text:
		return 0

	positive_words = ['great', 'excellent', 'good', 'amazing', 'happy', 'productive', 'efficient', 'helpful']
	negative_words = ['poor', 'bad', 'slow', 'inefficient', 'unhappy', 'difficult', 'issue', 'problem']

	text = text.lower()
	score = 0
	for word in positive_words:
		if word in text:
			score += 1
	for word in negative_words:
		if word in text:
			score -= 1

	# Normalize to 0-5
	normalized_score = 2.5 + (score * 0.5)
	return max(0, min(5, normalized_score))
