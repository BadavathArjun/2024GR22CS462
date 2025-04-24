import pandas as pd
import matplotlib.pyplot as plt
try:
    from ydata_profiling import ProfileReport
except ImportError:
    print("ydata-profiling not found, generating basic reports only")
    ProfileReport = None

# Read and preprocess data
data = []
with open("testfile_2025-04-19_23:35:14.csv") as f:
    for line in f:
        if line.strip().startswith(('0','1','2','3','4','5','6','7','8','9')):
            parts = line.strip().split(',')
            if len(parts) == 6:
                data.append(parts)

# Create DataFrame with network slices
df = pd.DataFrame(data, columns=["Channel", "Width", "GI", "MCS", "TxPower", "Throughput"])
df = df.apply(pd.to_numeric)
df['Slice'] = pd.cut(df['MCS'], 
                    bins=[0, 3, 7, 11],
                    labels=['BE (Best Effort)', 'VO (Voice)', 'VI (Video)'])

# 1. Throughput vs Channel Width by Slice
plt.figure(figsize=(12,6))
scatter = plt.scatter(df["Width"], df["Throughput"], c=df["MCS"], cmap="viridis")
plt.colorbar(scatter, label='MCS Index')
for slice_name, group in df.groupby('Slice'):
    plt.scatter(group["Width"], group["Throughput"], 
               label=slice_name, alpha=0.5, edgecolors='black')
plt.ylabel('Throughput (Mbps)')
plt.xlabel('Channel Width (MHz)')
plt.title("Network Slicing Performance")
plt.legend()
plt.grid(True)
plt.savefig("slicing_performance.png", bbox_inches='tight', dpi=300)
plt.close()

# 2. MCS Distribution by Slice
fig, axes = plt.subplots(1, 3, figsize=(15,5), sharey=True)
for ax, (slice_name, group) in zip(axes, df.groupby('Slice')):
    group['MCS'].hist(ax=ax, bins=20)
    ax.set_title(slice_name)
    ax.set_xlabel("MCS Index")
    if ax == axes[0]:
        ax.set_ylabel("Frequency")
fig.suptitle("MCS Distribution per Network Slice")
plt.savefig("mcs_by_slice.png", bbox_inches='tight', dpi=300)
plt.close()

# 3. QoS Comparison
plt.figure(figsize=(10,5))
df.boxplot(column='Throughput', by='Slice')
plt.title("Throughput Distribution by Slice Type")
plt.suptitle("")
plt.ylabel('Throughput (Mbps)')
plt.savefig("qos_comparison.png", bbox_inches='tight', dpi=300)
plt.close()

# 4. Generate comprehensive report (if ydata-profiling available)
if ProfileReport:
    profile = ProfileReport(df, 
                          title="WiFi Network Slicing Analysis",
                          correlations={"pearson": {"calculate": True},
                                      "spearman": {"calculate": True}})
    profile.to_file("network_slicing_report.html")
    print("\n✔ Full HTML report generated: network_slicing_report.html")
else:
    # Basic statistical summary
    with open("network_statistics.txt", "w") as f:
        f.write(str(df.groupby('Slice').describe()))
    print("\n✔ Basic statistics saved: network_statistics.txt")

print("""
Analysis complete! Created:
1. slicing_performance.png - Throughput vs Channel Width by slice
2. mcs_by_slice.png - MCS distribution per slice
3. qos_comparison.png - Throughput distribution comparison
""")
