from flask import Flask, render_template, request ,redirect, url_for
import paramiko
from urllib.parse import urlparse

import webbrowser
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static', methods=['POST'])
def modify_remote_script():
    # Get the form data from the request
    ip_address = request.form['ip_address']
    netmask = request.form['netmask']
    gateway = request.form['gateway']

    # Create an SSH client
    ssh = paramiko.SSHClient()

    # Automatically add the server's host key (this is insecure, only for demonstration)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote system
    ssh.connect('182.168.7.1', username='wlg', password='zxcv@123')

    # Command to configure the IP address
    command = f'sudo /home/wlg/.src/static.sh {ip_address} {netmask} {gateway}'
    

    # Execute the command on the remote system'
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    stdin.write('zxcv@123' + '\n')
    stdin.flush()
    # Print the output and error (if any)
    print(stdout.read().decode())
    print(stderr.read().decode())

    # Close the SSH connection
    ssh.close()

    return 'Static_Ip Successfully!'

@app.route('/dyanmic', methods=['POST'])
def execute_second_command():
    # Get the form data from the request
    # Add your form fields for the second command

    # Create an SSH client
    ssh = paramiko.SSHClient()

    # Automatically add the server's host key (this is insecure, only for demonstration)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote system
    ssh.connect('182.168.7.1', username='wlg', password='zxcv@123')

    command = f'sudo /home/wlg/.src/dyanmic.sh'
    

    # Execute the command on the remote system
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    stdin.write('zxcv@123' + '\n')
    stdin.flush()

    # Print the output and error (if any)
    print(stdout.read().decode())
    print(stderr.read().decode())

    # Close the SSH connection
    ssh.close()

    return 'Dyanmic_IP Successfully!'


@app.route('/search',methods=['GET','POST'])
def search():
    search_query = request.form['search']

    # Check if the search query is a valid URL or IP address
    parsed_url = urlparse(search_query)
    if parsed_url.netloc:
        # Open the specified URL or router IP address in the default web browser
        webbrowser.open(search_query)
    else:
        # Perform a Google search for other queries
        webbrowser.open('http://' + search_query)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
