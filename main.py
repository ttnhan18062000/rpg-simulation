import subprocess

servers = [
    "python game.py",
    "python kafka/push_to_mongodb.py",
    "npm run dev",
]

directories = ["game/", "data_streaming/", "dashboard/"]

processes = [
    subprocess.Popen(server, shell=True, cwd=dir)
    for server, dir in zip(servers, directories)
]

# Optionally, wait for all processes to finish
for process in processes:
    process.wait()
