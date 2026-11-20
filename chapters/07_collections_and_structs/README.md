# Chapter 07: Collections & Structs

This chapter introduces Mojo's standard library collection types and value `struct` semantics.

## Homogeneous `List[T]`
`List[T]` stores elements contiguously in memory for optimal CPU cache locality and SIMD processing:
```mojo
from std.collections import List

var items = List[Int]()
items.append(10)
items.append(20)
```

## Swiss-Table `Dict[Key, Value]`
Mojo's dictionary uses an advanced Swiss Table design with SIMD probing for high-performance associative mappings:
```mojo
from std.collections import Dict

var map = Dict[String, Int]()
map["port"] = 8000
```

## Zero-Cost `struct` Models
Unlike Python classes which allocate heap memory and dynamic dictionaries per instance, Mojo structs are flat value types with zero pointer indirection:
```mojo
struct Item:
    var id: Int
    var title: String

    def __init__(out self, id: Int, title: String):
        self.id = id
        self.title = title
```

## Running this Chapter
```bash
uv run mojo chapters/07_collections_and_structs/structs.mojo
```
