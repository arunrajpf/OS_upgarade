import subprocess

# Open a new HTML file for writing
with open("failedhost.html", "w") as output_file:
    # Write the heading
    output_file.write("<h2>PFB Failed node list</h2>")
    # Write the table start tag
    output_file.write("<table border='1'>")
    # Write the table header row
    output_file.write("<tr><th>Failed Node List</th></tr>")
    # Write the table data row
    with open("failed.host", "r") as file:
        hostname = file.read().strip()
        output_file.write(f"<tr><td>{hostname}</td></tr>")
    # Write the table end tag
    output_file.write("</table>")

# Read HTML content from the file
with open("failedhost.html", "r") as file:
    html_content = file.read()

# Additional body text
body_text = "Hello Unix team,\n\nPlease find below the list of failed hosts"

# Construct the plain text and HTML body
plain_text_body = f"{body_text}\n"
html_body = f"<html><body>{body_text}<br><br>{html_content}<br>Best Regards,<br>BSD-CORE</body></html>"

# Recipients
recipients="priya_palaniyappan@comcast.com bxtsre@comcast.com BSD_OPS_L2_UNIX_SA@comcast.com arun_raj2@comcast.com"
#recipients="priya_palaniyappan@comcast.com arun_raj2@comcast.com"

# Use a here document to provide the email content
email_content = f"""\
To: {recipients}
Subject: Failed Servers during Rocky Upgrade - Please fix the errors and try again
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
