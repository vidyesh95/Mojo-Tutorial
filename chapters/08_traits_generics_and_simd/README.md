# Chapter 08: Traits, Generics & SIMD Vectorization

This chapter dives into Mojo's compile-time abstraction and hardware-accelerated computing capabilities.

## Traits
A `trait` defines a set of required methods that a type must implement, similar to Rust traits or Go interfaces:
```mojo
trait Scorable:
    def compute_risk(self) -> Float64:
        ...
```

## Monomorphized Generics
Mojo generates specialized native assembly for every concrete type used with a generic function, eliminating the runtime dispatch overhead found in Python or Java:
```mojo
def print_score[T: Scorable](item: T):
    print(item.compute_risk())
```

## SIMD Vectorization
Hardware SIMD registers allow a single CPU instruction to perform mathematical operations across an entire vector of elements simultaneously:
```mojo
var v1 = SIMD[DType.float32, 4](1.0, 2.0, 3.0, 4.0)
var v2 = SIMD[DType.float32, 4](2.0, 2.0, 2.0, 2.0)
var result = v1 * v2  # Executed in a single hardware cycle
```

## Running this Chapter
```bash
uv run mojo chapters/08_traits_generics_and_simd/simd_compute.mojo
```
