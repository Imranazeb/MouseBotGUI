import base64

pic = open('favicon.ico', 'rb')
content = f'img = {base64.b64encode(pic.read())}\n'
pic.close()

with open('pic2str.py', 'w') as f:
    f.write(content)
