import subprocess

subnet = "10.9.138"

for i in range(65, 94):
    ip = f"{subnet}.{i}"
    try:
        result = subprocess.check_output(["ping", "-c", "1", ip])  # On Windows, replace "-c" with "-n"
        print(f"{ip} is online.")
    except subprocess.CalledProcessError:
        print(f"{ip} is offline.")