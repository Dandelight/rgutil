import subprocess
from sys import exc_info


def get_git_hash():
    try:
        return subprocess.check_output(["git", "describe", "--always"]).strip().decode()
    except:
        print(exc_info())
        return ""


def git_diff_cached(write_to_file=None):
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"], stdout=subprocess.PIPE, check=True
        )

        # Write the output as-i
        if write_to_file is not None:
            with open(write_to_file, "wb") as f:
                f.write(result.stdout)

        return result.stdout.decode()
    except:
        print(exc_info())
        return ""


def git_add_all():
    try:
        return subprocess.check_output(["git", "add", "--all"]).strip().decode()
    except:
        print(exc_info())
        return ""
