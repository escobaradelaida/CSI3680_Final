# this file will contain the decryption logic 
# it should be called when we press the decrypt button

from cryptography.fernet import Fernet

#load generated encryption key key.key file
with open('key.key', 'rb') as key_file:
    key = key_file.read()

# create fernet object with the key
cipher = Fernet(key)

# read the encrypted image
with open('medical_test.jpg', 'rb') as private_img_file:
    private_img = private_img_file.read()

# decrypt the image
decrypted_img = cipher.decrypt(private_img)

# write the decrypted image to a new file
with open('decrypted_img.jpg', 'wb') as decrypted_img_file:
    decrypted_img_file.write(decrypted_img)

print("The image has been decrypted and saved into decrypted_img.jpg")