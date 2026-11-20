# 07_collections_and_structs: Collections & Zero-Cost Structs

from std.collections import List, Dict

# Zero-cost value struct representing an application domain model
struct UserAccount(Copyable, Movable):
    var id: Int
    var username: String
    var email: String
    var is_active: Bool

    def __init__(out self, id: Int, username: String, email: String, is_active: Bool = True):
        self.id = id
        self.username = username
        self.email = email
        self.is_active = is_active

    def describe(self):
        print("User #", self.id, self.username, "<" + self.email + "> Active:", self.is_active)

def main():
    # 1. Working with dynamically-sized List[T]
    var items = List[String]()
    items.append("Mojo Compiler")
    items.append("FastAPI Engine")
    items.append("Better Auth Core")

    print("Collections - List count:", len(items))
    for item in items:
        print("  Item:", item)

    # 2. Swiss-table key-value Dict[Key, Value]
    var roles = Dict[String, String]()
    roles["alice@domain.com"] = "admin"
    roles["bob@domain.com"] = "user"
    print("Alice role:", roles.get("alice@domain.com").value())

    # 3. Initializing and using Structs
    var user1 = UserAccount(1, "alice", "alice@domain.com")
    user1.describe()
