import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", "--output-format=github", ".")


@nox.session(reuse_venv=True)
def test(session):
    session.install("-r", "requirements.txt")
    session.install(".")
    session.install("pytest")
    session.run("pytest")
