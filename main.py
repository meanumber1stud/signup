#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

form_variable = """
<!DOCTYPE html>

<html>
    <head>

    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error">{0}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">{1}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">{2}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email</label></td>
                    <td>
                        <input name="email" type="text" value="">
                        <span class="error">{3}</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>"""
def valid_username(username):
    User_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return User_RE.match(username)

def valid_password (password):
    Pword_RE = re.compile("^.{3,20}$")
    return Pword_RE.match(password)
def valid_email (email):
    Vemail = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    return Vemail.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        new_variable = form_variable.format("","","","")
        self.response.write(new_variable)

    def post(self):
        user = cgi.escape(self.request.get("username"))
        passWord = cgi.escape(self.request.get("password"))
        verify = cgi.escape(self.request.get("verify"))
        email = cgi.escape(self.request.get("email"))
        invalidUsernameOutput = ""
        if valid_username(user) == None:
            invalidUsernameOutput = "Invalid Username"

        invalidPasswordOutput =  ""
        nonMatchingPassword = ""
        invalidEmailOutput = ""

        if valid_email(email) == None:
            invalidEmailOutput = "Invalid Email"

        if valid_password(passWord) == None:
            invalidPasswordOutput = "Invalid password"
        else:
            if verify != passWord:
                nonMatchingPassword = "Passwords Do Not Match"
        if invalidUsernameOutput == "" and invalidPasswordOutput == "" and nonMatchingPassword == "" and invalidEmailOutput == "":
            self.redirect("/welcome?user=" + user)
        else:
            new_variable = form_variable.format(invalidUsernameOutput,invalidPasswordOutput,nonMatchingPassword,invalidEmailOutput)
            self.response.write(new_variable)


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        user = self.request.get("user")
        welcome_var = "Welcome " + user + "!"
        self.response.write(welcome_var)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomePage)
], debug=True)


"""type = password rather than text"""
