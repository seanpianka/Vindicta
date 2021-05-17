# Below is the reason for "-nolisten tcp" (this is not documented within Xvfb manpages)
# https://superuser.com/questions/855019/make-xvfb-listen-only-on-local-ip
Xvfb -ac :99 &
python3 vindicta.py
