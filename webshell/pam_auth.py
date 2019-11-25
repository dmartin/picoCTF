import os
import pwd
import signal
import subprocess
import time

import requests

USER_QUOTA_FILE = "/aquota.user"
USER_QUOTA = {
    "block_soft": "97M",
    "block_hard": "100M",
    "inode_soft": "2950",
    "inode_hard": "3000",
}
API_HOST = "http://api"
API_PORT = "8000"
TIMEOUT = 5

pamh = None


def authenticate(user, password):
    """Attempt to authenticate against the pico API."""
    res = requests.post(
        API_HOST + ":" + API_PORT + "/api/v1/user/login",
        headers={"user-agent": "pico toolbox"},
        json={"username": user, "password": password},
        timeout=TIMEOUT,
    )
    return res.json()


def display(string):
    message = pamh.Message(pamh.PAM_TEXT_INFO, string)
    pamh.conversation(message)


def prompt(string):
    message = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, string)
    return pamh.conversation(message)


def create_home_dir(user):
    subprocess.check_output(["/sbin/mkhomedir_helper", user])
    home = pwd.getpwnam(user).pw_dir

    # Append only bash history
    subprocess.check_output(["touch", os.path.join(home, ".bash_history")])
    subprocess.check_output(
        ["chown", "root:" + user, os.path.join(home, ".bash_history")]
    )
    subprocess.check_output(["chmod", "660", os.path.join(home, ".bash_history")])
    subprocess.check_output(["chattr", "+a", os.path.join(home, ".bash_history")])

    # Secure bashrc
    subprocess.check_output(
        ["cp", "/root/securebashrc", os.path.join(home, ".bashrc")])
    subprocess.check_output(["chown", "root:" + user, os.path.join(home, ".bashrc")])
    subprocess.check_output(["chmod", "755", os.path.join(home, ".bashrc")])
    subprocess.check_output(["chattr", "+a", os.path.join(home, ".bashrc")])

    # Secure profile
    subprocess.check_output(["chown", "root:" + user, os.path.join(home, ".profile")])
    subprocess.check_output(["chmod", "755", os.path.join(home, ".profile")])
    subprocess.check_output(["chattr", "+a", os.path.join(home, ".profile")])

    # User should not own their home directory
    subprocess.check_output(["chown", "root:" + user, home])
    subprocess.check_output(["chmod", "1770", home])

    # Ensure /home is not world-readable
    subprocess.check_output(["chmod", "o-r", "/home"])

    # Check if user quota is enabled, if so, add quota for this user
    if os.path.exists(USER_QUOTA_FILE):
        subprocess.check_output(
            [
                "/usr/sbin/setquota",
                user,
                USER_QUOTA["block_soft"],
                USER_QUOTA["block_hard"],
                USER_QUOTA["inode_soft"],
                USER_QUOTA["inode_hard"],
                "/",
            ]
        )


def pam_sm_authenticate(pam_handle, flags, argv):
    global pamh
    pamh = pam_handle

    # Ignore SIGINT instead of raising KeyboardException
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        username = pamh.get_user("Enter your pico account username: ")
    except pamh.exception:
        return pamh.PAM_AUTH_ERR
    pw_response = prompt(
        "Enter your pico account password (characters will be hidden): "
    )

    auth_response = authenticate(username, pw_response.resp)
    if (auth_response.get("success", False)):
        try:
            uid = auth_response['user']['shell_uid']
            subprocess.check_output(
                ["/usr/sbin/groupadd", "--gid", str(uid), username])
            subprocess.check_output(
                ["/usr/sbin/useradd", "-M", "--shell", "/bin/bash", "--uid", str(uid), "--gid", str(uid), username])
            if not os.path.isdir(pwd.getpwnam(username).pw_dir):
                create_home_dir(username)
            display("Welcome, {}!".format(username))
            return pamh.PAM_SUCCESS
        except subprocess.CalledProcessError:
            display("An internal error has occurred.")
            return pamh.PAM_AUTH_ERR
    else:
        time.sleep(3)
        return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS
