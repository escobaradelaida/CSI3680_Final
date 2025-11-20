# encrypting images
from cryptography.fernet import Fernet

# load the key from the key.key file
with open('key.key', 'rb') as key_file:
    key = key_file.read()

# create Fernet object with the key
cipher = Fernet(key)

# read image that will be encrypted. ideally, this would be connected to os package to be as a button to
# choose file
with open(r'C:\Users\ImBaby\Pictures\cat_loaf.jpg', 'rb') as image_file:
    img = image_file.read()

# encrypt image
private_img = cipher.encrypt(img)

# create a new file with the encrypted image in it
with open('medical_test.jpg', 'wb') as private_img_file:
    private_img_file.write(private_img)

print("The image has been encrypted successfully!")
