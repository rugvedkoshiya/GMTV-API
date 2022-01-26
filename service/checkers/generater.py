roleType = {
    0: "Member",
    1: "Worker",
    2: "Admin",
    3: "Super Admin",
}


def roleGenerator(role):
    return {
        "role": role,
        "roleName": roleType.get(role)
    }
