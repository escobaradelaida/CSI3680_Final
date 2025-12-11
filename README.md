[README.md](https://github.com/user-attachments/files/23509400/README.md)

# MediCrypt

MediCrypt is a Python program that allows users to upload an image and encrypts it using symmetric key cryptography methods before sending the image to its intended recipient. The recipient then uploads the encrypted image, and it is decrypted using the decryption key. The program is GUI-based and must be downloaded to the devices that need to encrypt/decrypt images.

## Purpose

We wanted to create a solution that reflects the need for privacy in the medical field. In theory, our program should encrypt sensitive medical files that need to be transfered through or outside the hospital network and ensure confidentiality.

## How to Run the Code

1. Save the GitHub repository to your local machine.
2. Navigate to the main project directory /CSI3680_Final-test/CSI3680_Final-test/ on your local machine.
3. To run the program, enter: python gui/main.py.
4. Test images can be found under /test_images directory for encrypting.

## Dependencies

The following python libraries must be installed to run the program:
1. tkinter
2. PIL
3. bcrypt 
4. Fernet

This can be done using pip.

On Windows:
pip install <library_name>

On macOS:
pip3 install <library_name>

## Key Classes and Functions

The App class manages page creation and layout as well as switching between pages. The EncryptPage and DecryptPage classes handle the encryption and decrpytion processes, respectively, using the Fernet module. The save_credentials() and verify_credentials functions handle account registration and login processes. The hash_password() function hashes the passwords supplied using the bcrypt module.

## Team Members and Contributions

Adelaida: Created the Tkinter frame that holds the application and coded the “frames” used to navigate through each section.

Danielle: Coded the encryption and decryption processes for the images and added hashes to user passwords for more security.
