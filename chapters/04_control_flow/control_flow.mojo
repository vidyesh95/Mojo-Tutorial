# 04_control_flow: Conditionals & Loops

def main():
    # 1. If / Elif / Else Branching
    var request_status: Int = 200
    if request_status == 200:
        print("Status: 200 OK")
    elif request_status == 404:
        print("Status: 404 Not Found")
    else:
        print("Status: Unknown code")

    # 2. For loop with range
    print("Processing batch batches 0..5:")
    var total_processed: Int = 0
    for i in range(5):
        total_processed += i
        print("  Processing index:", i)
    print("Total accumulated:", total_processed)

    # 3. While loop with break and continue
    var step: Int = 0
    while step < 10:
        step += 1
        if step == 2:
            continue
        if step > 4:
            break
        print("  While step:", step)

    # 4. Compile-time branching with if comptime(...)
    comptime OPTIMIZE_FOR_SERVER = True
    if comptime(OPTIMIZE_FOR_SERVER):
        print("Compiled with server optimization enabled!")
