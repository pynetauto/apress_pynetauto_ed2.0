import subprocess
import os
import time

# Record the start time
start_time = time.time()

#####################################################

# Function to run a shell command and print its output
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip()  # Get the command output
        print(output)
        print(f"Command executed successfully: {command}")
        return output  # Return the output
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error details: {e.stderr}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

print("#1~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 1. Update the Linux server
update_command = "sudo apt update"
run_command(update_command)

print("#2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 2. Install PostgreSQL
install_postgresql_command = "sudo apt install -y postgresql"
run_command(install_postgresql_command)

print("#4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 4. Start and enable PostgreSQL service
start_postgresql_command = "sudo systemctl start postgresql"
enable_postgresql_command = "sudo systemctl enable postgresql"
run_command(start_postgresql_command)
run_command(enable_postgresql_command)

print("#5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 5. Create a database and user, and grant privileges
create_db_user_command = '''
sudo -u postgres psql -c "CREATE DATABASE netbox;"
sudo -u postgres psql -c "CREATE USER netbox WITH PASSWORD 'P0stgr3SQLP@ss!';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;"
'''
run_command(create_db_user_command)

print("#7~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 7. Install Redis
install_redis_command = "sudo apt install -y redis-server"
run_command(install_redis_command)

# 7b. Start Redis service
start_redis_command = "sudo service redis-server start"
run_command(start_redis_command)

# 7c. Enable Redis service to start on boot
enable_redis_service_command = "sudo systemctl enable redis-server"
run_command(enable_redis_service_command)

# 7d. Check Redis version
check_redis_version_command = "redis-server -v"
run_command(check_redis_version_command)

print("#8~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 8. Install NetBox dependencies
install_dependencies_command = '''
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential libxml2-dev libxslt1-dev libffi-dev libpq-dev libssl-dev zlib1g-dev
'''
run_command(install_dependencies_command)

print("#9~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 9. Create the NetBox directory and clone the repository
create_netbox_directory_command = "sudo mkdir -p /opt/netbox/"
run_command(create_netbox_directory_command)

# 9b. Change the working directory to '/opt/netbox'
os.chdir("/opt/netbox/")

# 9c. Install Git
install_git_command = "sudo apt install -y git"
run_command(install_git_command)

# 9d. Clone the NetBox repository (latest version)
clone_netbox_command = "sudo git clone -b master --depth 1 https://github.com/netbox-community/netbox.git ."
run_command(clone_netbox_command)

print("#10~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 10. Create NetBox system user and change the ownership of the media directory for any device images to be used.
create_netbox_user_command = "sudo adduser --system --group netbox"
change_media_ownership_command = "sudo chown --recursive netbox /opt/netbox/netbox/media/"
run_command(create_netbox_user_command)
run_command(change_media_ownership_command)

print("#11~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 11. Change directory, copy example configuration file, and then modify it.
os.chdir("/opt/netbox/netbox/netbox/")
copy_config_file_command = "sudo cp configuration_example.py configuration.py"
run_command(copy_config_file_command)

print("#12~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 12a. Update configuration.py file with the SQL user and password.
print("# 12. Update configuration.py file with the SQL user and password.")
# Define the path to the configuration.py file
config_file_path = '/opt/netbox/netbox/netbox/configuration.py'
# Read the existing configuration.py file
with open(config_file_path, 'r') as config_file:
    lines = config_file.readlines()
# Update 'USER' and 'PASSWORD' values (only the first instance)
updated_lines = []
user_updated = False
password_updated = False

for line in lines:
    if not user_updated and line.strip().startswith("'USER':"):
        updated_lines.append(f"    'USER': 'netbox',\n")
        user_updated = True
    elif not password_updated and line.strip().startswith("'PASSWORD':"):
        updated_lines.append(f"    'PASSWORD': 'P0stgr3SQLP@ss!',\n")
        password_updated = True
    else:
        updated_lines.append(line)

# Write the updated lines back to the configuration.py file
with open(config_file_path, 'w') as config_file:
    config_file.writelines(updated_lines)

# 12b. Use Python to generate a secret key and append it to the configuration.py file
print("# 12b. Generating a secret key...")
generate_secret_key_command = "python3 /opt/netbox/netbox/generate_secret_key.py"
generated_secret_key = run_command(generate_secret_key_command)
if generated_secret_key is not None:
    print("# Generated Secret Key:", generated_secret_key)
    # Append the "SECRET_KEY = generated_secret_key" to the end of configuration.py file
    print("# Appending the SECRET_KEY to the configuration.py file...")
    # Replace with the actual generated secret key
    append_secret_key_command = f"sudo echo 'SECRET_KEY = \"{generated_secret_key}\"' >> /opt/netbox/netbox/netbox/configuration.py"
    run_command(append_secret_key_command)

print("#13~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 13. Append 'napalm' to local_requirements.txt
append_napalm_command = "sudo sh -c \"echo 'napalm' >> /opt/netbox/local_requirements.txt\""
run_command(append_napalm_command)

print("#14~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 14. Run the upgrade script
print("# 14. Running the upgrade script...")
run_upgrade_script_command = "sudo /opt/netbox/upgrade.sh"
run_command(run_upgrade_script_command)

print("#15~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 15. Activating the virtual environment
print("# 15. Activating the virtual environment...")
activate_venv_command = "source /opt/netbox/venv/bin/activate"
subprocess.run(activate_venv_command, shell=True, text=True)
change_dir = "cd /opt/netbox/netbox"
subprocess.run(change_dir, shell=True, text=True)

print("#16~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 16. Define the command to create a superuser
createsuperuser_command = "python3 manage.py createsuperuser"

# Define the responses
responses = {
    "Username (leave blank to use 'root'): ": "admin\n",
    "Email address: ": "admin@pynetauto.com\n",
    "Password: ": "admin\n",
    "Password (again): ": "admin\n",
}

try:
    # Run the command and provide responses interactively
    process = subprocess.Popen(
        createsuperuser_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )

    for prompt, response in responses.items():
        response_str = f"{response}"
        process.stdin.write(response_str)
        process.stdin.flush()

    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("Superuser created successfully.")
    else:
        print(f"Error creating superuser: {stderr}")
except Exception as e:
    print(f"An error occurred: {e}")

print("#18~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 18. Define the path to the settings.py file
settings_file_path = '/opt/netbox/netbox/netbox/settings.py'

print("#19~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 19. Define the new ALLOWED_HOSTS line
new_allowed_hosts_line = "ALLOWED_HOSTS = ['*']\n"

try:
    # Read the existing content of settings.py
    with open(settings_file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    found_allowed_hosts = False
    print("#20~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # 20. Iterate through the lines and update ALLOWED_HOSTS
    for line in lines:
        if line.strip().startswith('ALLOWED_HOSTS'):
            updated_lines.append(new_allowed_hosts_line)
            found_allowed_hosts = True
        else:
            updated_lines.append(line)

    # If ALLOWED_HOSTS was not found, append it to the end of the file
    if not found_allowed_hosts:
        updated_lines.append(new_allowed_hosts_line)
    print("#21~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # 21. Write the modified content back to settings.py
    with open(settings_file_path, 'w') as file:
        file.writelines(updated_lines)

    print("ALLOWED_HOSTS updated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

print("#22~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 22. Command to copy the gunicorn.py file
copy_gunicorn_command = "sudo cp /opt/netbox/contrib/gunicorn.py /opt/netbox/gunicorn.py"

try:
    # Copy the gunicorn.py file
    subprocess.run(copy_gunicorn_command, shell=True, text=True, check=True)
    print("gunicorn.py file copied successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error copying gunicorn.py file: {e.stderr}")
except Exception as e:
    print(f"An error occurred: {e}")

print("#23~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 23. Commands to copy .service files, reload systemd, start, and enable NetBox services
copy_service_files_command = "sudo cp -v /opt/netbox/contrib/*.service /etc/systemd/system/"
reload_systemd_command = "sudo systemctl daemon-reload"
start_netbox_command = "sudo systemctl start netbox netbox-rq"
enable_netbox_command = "sudo systemctl enable netbox netbox-rq"

try:
    # Copy .service files
    subprocess.run(copy_service_files_command, shell=True, text=True, check=True)
    print("Service files copied successfully.")

    # Reload systemd
    subprocess.run(reload_systemd_command, shell=True, text=True, check=True)
    print("Systemd reloaded successfully.")

    # Start NetBox services
    subprocess.run(start_netbox_command, shell=True, text=True, check=True)
    print("NetBox services started successfully.")

    # Enable NetBox services to start on boot
    subprocess.run(enable_netbox_command, shell=True, text=True, check=True)
    print("NetBox services enabled successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e.stderr}")
except Exception as e:
    print(f"An error occurred: {e}")

# ==============================================================
print("#24~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 24. Create a local SSL certificate and define the openssl command with default values for prompts
openssl_command = (
    "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 "
    "-keyout /etc/ssl/private/netbox.key "
    "-out /etc/ssl/certs/netbox.crt"
)

# Create a dictionary of responses to provide default values for prompts
responses = {
    "Country Name (2 letter code) [AU]:": "\n",
    "State or Province Name (full name) [Some-State]:": "\n",
    "Locality Name (eg, city) []:": "\n",
    "Organization Name (eg, company) [Internet Widgits Pty Ltd]:": "\n",
    "Organizational Unit Name (eg, section) []:": "\n",
    "Common Name (e.g. server FQDN or YOUR name) []:": "\n",
    "Email Address []:": "\n",
}

try:
    # Run the openssl command and provide responses interactively
    process = subprocess.Popen(
        openssl_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )

    for prompt, response in responses.items():
        response_str = f"{response}"
        process.stdin.write(response_str)
        process.stdin.flush()

    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("Local SSL certificate created successfully.")
    else:
        print(f"Error creating SSL certificate: {stderr}")
except Exception as e:
    print(f"An error occurred: {e}")

#==============================================================
print("#25~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 25. Install Nginx
install_nginx_command = "sudo apt install -y nginx"

try:
    # Run the command to install Nginx
    subprocess.run(install_nginx_command, shell=True, text=True, check=True)
    print("Nginx installed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error installing Nginx: {e.stderr}")
except Exception as e:
    print(f"An error occurred: {e}")

#==============================================================
print("#26~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 26. Create and configure the Nginx site file
nginx_config_content = '''
server {
    listen [::]:443 ssl ipv6only=off;

    # CHANGE THIS TO YOUR SERVER'S NAME
    server_name 192.168.127.20;

    ssl_certificate /etc/ssl/certs/netbox.crt;
    ssl_certificate_key /etc/ssl/private/netbox.key;

    client_max_body_size 25m;

    location /static/ {
        alias /opt/netbox/netbox/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    # Redirect HTTP traffic to HTTPS
    listen [::]:80 ipv6only=off;
    server_name _;
    return 301 https://$host$request_uri;
}
'''

# Create and write the Nginx site configuration file
nginx_config_path = '/etc/nginx/sites-available/netbox'
with open(nginx_config_path, 'w') as nginx_config_file:
    nginx_config_file.write(nginx_config_content)

# Print success message
print("Nginx site configuration created successfully.")

#==============================================================
print("#27~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 27. Delete the Nginx default site and create a symlink to the new active file
delete_default_nginx_site_command = "sudo rm /etc/nginx/sites-enabled/default"
create_symlink_command = "sudo ln -s /etc/nginx/sites-available/netbox /etc/nginx/sites-enabled/netbox"

# Delete the default site and create the symlink
run_command(delete_default_nginx_site_command)
run_command(create_symlink_command)

# Print success messages
print("Default Nginx site deleted and symlink created successfully.")
#==============================================================

# 28. Restart the Nginx service
print("#28~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
restart_nginx_command = "sudo systemctl restart nginx"

# Restart the Nginx service
run_command(restart_nginx_command)

# Print a success message
print("Nginx service restarted successfully.")

#####################################################
# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Script execution time: {elapsed_time} seconds")