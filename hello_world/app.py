import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VanityNumbers')

# Function to generate vanity numbers
def generate_vanity_numbers(phone_number):
    # Placeholder function for converting phone number to vanity numbers
    # Implement your logic here
    vanity_numbers = ["CALLME", "FUN123", "HELLO9", "FOOD45", "SHOP67"]
    return vanity_numbers

def lambda_handler(event, context):
    try:
        # Extract the phone number from the event
        phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']
        
        # Generate vanity numbers
        vanity_numbers = generate_vanity_numbers(phone_number)
        
        # Choose the top 5 vanity numbers based on custom criteria
        best_vanity_numbers = vanity_numbers[:5]
        
        # Save to DynamoDB
        table.put_item(
            Item={
                'PhoneNumber': phone_number,
                'VanityNumbers': best_vanity_numbers
            }
        )
        
        # Return the top 3 vanity numbers for the contact flow
        return {
            'statusCode': 200,
            'body': json.dumps(best_vanity_numbers[:3])
        }
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error saving to DynamoDB')
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('An unknown error occurred')
        }
