from string import Template

# A cancelled mpesa request body
cancelledResponse = Template('''
{
  'Body': {
    'stkCallback': {
      'MerchantRequestID': '8555-67195-1',
      'CheckoutRequestID': '$CheckoutRequestID',
      'ResultCode': 1032,
      'ResultDesc': '[STK_CB - ]Request cancelled by user',
    },
  },
}
''')

# An accepted mpesa request body
acceptedResponse = Template('''
{
  'Body': {
    'stkCallback': {
      'MerchantRequestID': '19465-780693-1',
      'CheckoutRequestID': '$CheckoutRequestID',
      'ResultCode': 0,
      'ResultDesc': 'The service request is processed successfully.',
      'CallbackMetadata': {
        'Item': [
          {
            'Name': 'Amount',
            'Value': 1,
          },
          {
            'Name': 'MpesaReceiptNumber',
            'Value': 'LGR7OWQX0R',
          },
          {
            'Name': 'Balance',
          },
          {
            'Name': 'TransactionDate',
            'Value': 20170727154800,
          },
          {
            'Name': 'PhoneNumber',
            'Value': 254721566839,
          },
        ],
      },
    },
  },
}
''')

