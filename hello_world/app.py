import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VanityNumbers')

# Function to map digits to letters for vanity numbers
digit_to_letters = {
    '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL', '6': 'MNO',
    '7': 'PQRS', '8': 'TUV', '9': 'WXYZ'
}

def generate_vanity_numbers(phone_number):
    def backtrack(index, path):
        if index == len(phone_number):
            result.append(''.join(path))
            return
        digit = phone_number[index]
        if digit in digit_to_letters:
            for letter in digit_to_letters[digit]:
                path.append(letter)
                backtrack(index + 1, path)
                path.pop()
        else:
            path.append(digit)
            backtrack(index + 1, path)
            path.pop()

    result = []
    backtrack(0, [])
    return result

def lambda_handler(event, context):
    try:
        # Extract the phone number from the event
        phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']
        
        # Generate vanity numbers
        vanity_numbers = generate_vanity_numbers(phone_number)
        
        # Choose the top 5 vanity numbers
        best_vanity_numbers = vanity_numbers[:5]
        
        # Save to DynamoDB
        table.put_item(
            Item={
                'PhoneNumber': phone_number,
                'VanityNumber1': vanity_numbers[0],
                'VanityNumber2': vanity_numbers[1],
                'VanityNumber3': vanity_numbers[2]
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
