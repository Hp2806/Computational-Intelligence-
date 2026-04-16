def get_activation(yin):
    if yin > 0:
        return 1
    elif yin == 0:
        return 0
    else:
        return -1
print("=" * 55)
print("       PERCEPTRON LEARNING ALGORITHM")
print("=" * 55)
n = int(input("Enter number of inputs (n)       : "))
print(f"\nEnter {2**n} input combinations and their targets:")
inputs  = []
targets = []
for i in range(2**n):
    vals = input(f"  Enter input {i+1} ({n} values space-separated): ").split()
    inputs.append(tuple(int(v) for v in vals))
    t = int(input(f"  Enter target for {inputs[-1]}           : "))
    targets.append(t)
weights = []
for i in range(n):
    w = float(input(f"Enter initial weight w{i+1}          : "))
    weights.append(w)
b      = float(input("Enter initial bias b              : "))
alpha  = float(input("Enter learning rate (alpha)       : "))
epochs = int(input("Enter max number of epochs       : "))
converged_epoch = None
for epoch in range(1, epochs + 1):
    print(f"\n\n{'='*85}")
    print(f"  EPOCH {epoch} CALCULATION DETAILS")
    print(f"{'='*85}")
    epoch_rows = []
    all_correct = True
    for i in range(len(inputs)):
        xs = inputs[i]
        t  = targets[i]
        yin = b + sum(xs[j] * weights[j] for j in range(n))
        y = get_activation(yin)
        dw = [0] * n
        db = 0
        if y != t:
            all_correct = False
            dw = [alpha * t * xs[j] for j in range(n)]
            db = alpha * t
            for j in range(n):
                weights[j] += dw[j]
            b += db
        row = list(xs) + [t, round(yin,2), y] + dw + [db] + [round(w,2) for w in weights] + [round(b,2)]
        epoch_rows.append(row)
        print(f"Pattern {i+1}: Input{xs} Target({t}) -> yin={round(yin,2)}, y={y} | {'OK' if y==t else 'Update Weights'}")
    print(f"\n  --- EPOCH {epoch} SUMMARY TABLE ---")
    x_headers  = "".join([f"{'x'+str(j+1):>5}" for j in range(n)])
    dw_headers = "".join([f"{'dw'+str(j+1):>6}" for j in range(n)])
    w_headers  = "".join([f"{'w'+str(j+1):>7}" for j in range(n)])
    header = f"{x_headers}{'t':>5}{'yin':>7}{'y':>5}{dw_headers}{'db':>6}{w_headers}{'b':>7}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    for r in epoch_rows:
        x_vals  = "".join([f"{v:>5}" for v in r[0:n]])
        t_val   = f"{r[n]:>5}"
        yin_val = f"{r[n+1]:>7}"
        y_val   = f"{r[n+2]:>5}"
        dw_vals = "".join([f"{v:>6}" for v in r[n+3:n+3+n]])
        db_val  = f"{r[n+3+n]:>6}"
        wf_vals = "".join([f"{v:>7}" for v in r[n+4+n:n+4+2*n]])
        bf_val  = f"{r[n+4+2*n]:>7}"
        print(f"{x_vals}{t_val}{yin_val}{y_val}{dw_vals}{db_val}{wf_vals}{bf_val}")
    if all_correct:
        converged_epoch = epoch
        break
print(f"\n{'='*40}")
print("  FINAL RESULTS")
print(f"{'='*40}")
if converged_epoch:
    print(f"Converged successfully in {converged_epoch} epoch(s).")
else:
    print(f"Reached max epochs ({epochs}) without full convergence.")

for j in range(n):
    print(f"Final w{j+1} : {round(weights[j], 4)}")
print(f"Final bias: {round(b, 4)}")
print(f"{'='*40}")
