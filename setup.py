api_key = input('Enter the api key for Yandex geocoder ')
with open('.env', 'w', encoding='utf-8') as file_env:
    file_env.write('API_KEY={}'.format(api_key))
print('Setup script completed successfully')