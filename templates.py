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

# nginx proxy pass to localhost configuration
proxy_to_localhost_nginx_conf = Template('''
# server

server{  
    # SSL Configuration
    server_name $server_name;
    client_max_body_size 5M;

    access_log  /var/log/nginx/$server_name.access.log;
    error_log   /var/log/nginx/$server_name.error.log;

    location / {
        proxy_pass http://127.0.0.1:$port/;
        proxy_read_timeout 1800;
        proxy_connect_timeout 1800;
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;
    }
}
''')

# nginx proxy pass to localhost configuration
static_server_with_proxy_nginx_conf = Template('''
# server
server{  
    # SSL Configuration
    server_name $server_name;
    client_max_body_size 5M;

    access_log  /var/log/nginx/$server_name.access.log;
    error_log   /var/log/nginx/$server_name.error.log;

    location /api/ {
        proxy_pass $proxy_pass/;
    }
}

''')


