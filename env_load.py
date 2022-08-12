import os


def env_load():
    print("loaded env values")
    print(os.environ.get("GIT_PR_NUMBER"), "PR Number")
    print(os.environ.get("GIT_REPOSITORY_NAME"), "Repo name")

if __name__ == "__main__":
    env_load()