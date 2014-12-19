from django.contrib.auth.backends import RemoteUserBackend

class Krb5RemoteUserBackend(RemoteUserBackend):
    def clean_username(self, username):
        # remove @REALM from username
        return username.split("@")[0] 