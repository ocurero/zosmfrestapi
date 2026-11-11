from zosmfrestapi.models.topology import Group, System


def make_group(name, systems=[]):
    return Group(
        name=name, description=f"A simple group called {name}", systems=",".join(systems)
    )


def make_system(name="", groups=[]):
    return System(
        name=f"TST{name}",
        nickName=f"TEST{name}",
        sysplex="TST01",
        groups=",".join(groups),
        jesType="JES2",
        jesMemberName=f"TST{name}",
        url="https://zosmf.example/zosmf/",
    )
