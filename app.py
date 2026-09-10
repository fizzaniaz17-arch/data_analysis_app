import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("AI LAB Python Check")
st.write("Pandas, matplotlib, and Streamlit are installed and working.")

# Create a sample DataFrame
sample_data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [85, 92, 78],
}
df = pd.DataFrame(sample_data)

st.subheader("Sample DataFrame")
st.dataframe(df)

# Create and display a simple plot
fig, ax = plt.subplots()
ax.plot(df["Name"], df["Score"], marker="o")
ax.set_title("Sample Scores")
ax.set_xlabel("Name")
ax.set_ylabel("Score")

st.pyplot(fig)
