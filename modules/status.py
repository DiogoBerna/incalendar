import json

def get_status():
	return {
		'statusCode': 200,
		'body': json.dumps('Everything in Its Right Place!')
	}
