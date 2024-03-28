import nox


@nox.session
def test(session):
    session.install(".")
    session.run("pytest")


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", ".")
