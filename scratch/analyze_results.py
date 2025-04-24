import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read and preprocess data
with open("testfile_2025-04-19_23:35:14.csv") as f:
    lines = [line.strip() for line in f if line.count(',') >= 4 and line[0].isdigit()]

df = pd.DataFrame([line.split(',') for line in lines]).astype(float)
df.columns = ["channelNumber", "channelWidth", "gi", "mcs", "txPower"]

# Plot 1: Channel Characteristics
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="channelWidth", y="txPower", hue="channelNumber", 
                size="mcs", palette="viridis")
plt.title("Channel Configuration Analysis")
plt.xlabel("Channel Width (MHz)")
plt.ylabel("Transmit Power (dBm)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("channel_analysis.png")
plt.close()

# Plot 2: MCS Distribution
plt.figure(figsize=(8, 5))
df["mcs"].plot(kind='hist', bins=20, edgecolor='black')
plt.title("MCS Index Distribution")
plt.xlabel("MCS Index")
plt.ylabel("Frequency")
plt.savefig("mcs_distribution.png")
plt.close()

# Plot 3: Parameter Relationships
sns.pairplot(df[["channelWidth", "txPower", "mcs"]])
plt.suptitle("Parameter Relationships", y=1.02)
plt.savefig("parameter_relationships.png")
plt.close()

print("Analysis complete! Created 3 plots:")
print("- channel_analysis.png")
print("- mcs_distribution.png")
print("- parameter_relationships.png")
