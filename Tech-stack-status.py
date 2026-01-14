import subprocess

# Read the content of final-merged_file.txt
with open('/ansible/app/platform/patch_val-test/final-merged_file.txt', 'r') as file:
    file_content = file.readlines()

# Constructing HTML table content
html_table_content = "<table border='1'><tr><th>Host name</th><th>Tech-stack Status</th></tr>"
for i in range(0, len(file_content), 3):
    pre_opens = file_content[i].strip().split(': ')[1]
    pre_uptycs = file_content[i+1].strip().split(': ')[1]
    pre_vname = file_content[i+2].strip().split(': ')[1]
    html_table_content += f"<tr><td>{pre_vname}</td><td>pre-opens: {pre_opens}, pre-uptycs: {pre_uptycs}</td></tr>"
html_table_content += "</table>"

# Additional body text
body_text = "Hello Unix team,\n\nPlease find the status of tech stack"

# Construct the plain text and HTML body
plain_text_body = f"{body_text}\n"
html_body = f"<html><body>{body_text}<br><br>{html_table_content}<br>Best Regards,<br>BSD-CORE</body></html>"

# Recipients
recipients = "priya_palaniyappan@comcast.com, bxtsre@comcast.com, BSD_OPS_L2_UNIX_SA@comcast.com, arun_raj2@comcast.com"

# Use a here document to provide the email content
email_content = f"""\
To: {recipients}
Subject: Tech stack staus-Before OS upgrade
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary=boundary_123456789

--boundary_123456789
Content-Type: text/plain; charset=ISO-8859-1
Content-Disposition: inline

{plain_text_body}

--boundary_123456789
Content-Type: text/html; charset=ISO-8859-1
Content-Disposition: inline

{html_body}

--boundary_123456789--
"""

# Send email via sendmail
try:
    process = subprocess.Popen(['/usr/sbin/sendmail', '-t'], stdin=subprocess.PIPE)
    process.communicate(input=email_content.encode())
    print(f"Email sent to all recipients: {recipients}")
except Exception as e:
    print("An error occurred:", e)
