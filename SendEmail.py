import smtplib
from email.mime.text import MIMEText
_to = "1107168572@qq.com"
_pwd  = "jidaozhilong12@#"
_user   = "18721173353@189.cn"

msg = MIMEText("Test")
msg["Subject"] = "don't panic"
msg["From"]    = _user
msg["To"]      = _to

try:
    s = smtplib.SMTP_SSL("smtp.189.cn")
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.quit()
    print "Success!"
except smtplib.SMTPException,e:
    print "Falied,%s"%e 
