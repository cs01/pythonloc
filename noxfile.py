import nox  # type: ignore


@nox.session()
def publish(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("build", "twine")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "-m", "build")
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
