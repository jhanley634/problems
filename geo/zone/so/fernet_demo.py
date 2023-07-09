#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/285976/password-recognition-with-cryptography

import json

from cryptography.fernet import Fernet
from pypasswords import hash_it, match_it


def base_generator(password: str):
    """
    Generates key and salt with password and then rehashes to make a derived key.
    This derived key is then saved in a dictionary with the salt for further security
    This one must get the password, if they want to get in.

    dictionary = {'main': {'derived_key': derived_key, 'salt': salt}}
    """

    key, salt = hash_it(password, salting=True)
    derived_key = hash_it(key)
    json_save = {'main': {'derived_key': derived_key, 'salt': salt}}

    return json_save


def re_hash(json_save: dict):
    """
    Re-encrypts the values with the key for further security if any at all as the key is still saved
    in the dictionary.

    dictionary = {'main': {'derived_key': derived_key, 'salt': salt, 'key': key}}
    """

    key = Fernet.generate_key()
    json_save['main']['derived_key'] = (
        Fernet(key).encrypt(json_save['main']['derived_key'].encode()).decode()
    )
    json_save['main']['salt'] = (
        Fernet(key).encrypt(json_save['main']['salt'].encode()).decode()
    )
    json_save['main']['key'] = key.decode()

    return json_save


def password_hasher(password: str):
    """
    Combination of 'base_generator' and 're_hash'
    """

    json_save = base_generator(password)
    json_save = re_hash(json_save)

    return json_save


def password_checker(json_save, password):
    """
    Basically undoes all the hashing and checks if password and salt equal to derived key
    """

    # Converting rehashed values back to originals
    key = json_save['main']['key'].encode()
    salt = Fernet(key).decrypt(json_save['main']['salt'].encode()).decode()
    derived_key = (
        Fernet(key).decrypt(json_save['main']['derived_key'].encode()).decode()
    )

    # Preparing for password confirmation
    password_key, salt = hash_it(password, salting=True, static_salt=salt)

    # Checking for password_confirmation with derived_key
    return match_it(password_key, derived_key)


def json_file(command, json_data):
    if command in ['dump', 'load']:
        if command == 'dump':
            with open('data.json', 'w') as data_file:
                json.dump(json_data, data_file, indent=4)

        if command == 'load':
            with open('data.json', 'r') as data_file:
                json_save = json.load(data_file)

            return json_save

    else:
        print('Invalid Command. Try "load", "dump"')


def main():
    password1 = input('Password: ')
    password2 = input('What was password? ')
    json_save = password_hasher(password1)

    json_file('dump', json_save)
    json_save = json_file('load', json_save)

    print(password_checker(json_save, password2))
    print(password1, password2, json_save)


if __name__ == '__main__':
    main()
