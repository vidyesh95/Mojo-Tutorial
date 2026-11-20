# 08_traits_generics_and_simd: Traits, Monomorphized Generics & SIMD

from std.collections import List

# 1. Defining an interface trait
trait Scorable:
    def compute_risk(self) -> Float64:
        ...

# 2. Implementing the trait in a domain struct
struct RiskProfile(Scorable):
    var credit_factor: Float64
    var delinquency_count: Int

    def __init__(out self, credit_factor: Float64, delinquency_count: Int):
        self.credit_factor = credit_factor
        self.delinquency_count = delinquency_count

    def compute_risk(self) -> Float64:
        return self.credit_factor * (1.0 + Float64(self.delinquency_count) * 0.25)

# 3. Monomorphized generic function bounded by trait
def evaluate_risk[T: Scorable](profile: T):
    print("Evaluated Risk Score:", profile.compute_risk())

def main():
    var client_profile = RiskProfile(0.85, 2)
    evaluate_risk(client_profile)

    # 4. Native SIMD (Single Instruction, Multiple Data) Vectorization
    # Process 4 float32 numbers simultaneously in a single CPU register instruction
    var vector_a = SIMD[DType.float32, 4](10.0, 20.0, 30.0, 40.0)
    var vector_b = SIMD[DType.float32, 4](1.5, 2.0, 0.5, 1.2)
    var vector_res = vector_a * vector_b

    print("SIMD vector input A:", vector_a)
    print("SIMD vector input B:", vector_b)
    print("SIMD vectorized product (single CPU instruction):", vector_res)
