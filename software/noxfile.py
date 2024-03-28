import nox


@nox.session
def test(session):
    session.install(".")
    session.run("pytest")
