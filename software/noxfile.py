import nox


@nox.session
def test(session):
    session.install("-r", "requirements.txt")
    session.install(".")
    session.install("pytest")
    session.run("pytest")


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", "--output-format=github", ".")
