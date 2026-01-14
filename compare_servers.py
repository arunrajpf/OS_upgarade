def update_hosts_file(hosts_file, failed_hosts_file):
    try:
        with open(hosts_file, 'r') as hosts:
            hosts_content = hosts.readlines()

        with open(failed_hosts_file, 'r') as failed_hosts:
            failed_hosts_content = set(line.strip() for line in failed_hosts.readlines())

        updated_hosts = [host for host in hosts_content if host.strip() not in failed_hosts_content]

        print(f"Original hosts content: {hosts_content}")
        print(f"Failed hosts content: {failed_hosts_content}")
        print(f"Updated hosts content: {updated_hosts}")

        with open(hosts_file, 'w') as hosts:
            hosts.writelines(updated_hosts)

        print("Hosts file updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Assuming the files are in the same directory as the script
update_hosts_file('hosts', 'failed.host')
