# This script is to run a fake mail and test the email logger

python -m smtpd -n -c DebuggingServer localhost:8025