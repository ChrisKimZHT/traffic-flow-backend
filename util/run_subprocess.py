import subprocess


def run_subprocess(cmd):
    return subprocess.run(cmd, shell=True, check=True)


def run_subprocess_with_callback(cmd, callback):
    try:
        completed_process = subprocess.run(cmd, shell=True, check=True)
        return_value = completed_process.returncode
    except subprocess.CalledProcessError as e:
        return_value = e.returncode
    callback(return_value)
