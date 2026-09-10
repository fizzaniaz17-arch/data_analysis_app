# lab_eda_gui.py

import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns


# ============================================================
# 1. Page Configuration
# ============================================================
st.set_page_config(page_title="data_analysist", layout="wide")
st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")


# ============================================================
# 2. Sidebar: Dataset Ingestion
# ============================================================

st.sidebar.header("Dataset controls")

# Create a file uploader in the sidebar for CSV files
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


# ============================================================
# Check whether a file has been uploaded
# ============================================================

if uploaded_file is not None:

    # --------------------------------------------------------
    # Read and validate dataset
    # --------------------------------------------------------

    try:
        df = pd.read_csv(uploaded_file)

        # Check whether dataset contains columns
        if df.empty or len(df.columns) == 0:
            st.error("The uploaded CSV file is empty.")
            st.stop()

    except Exception as e:
        st.error("Invalid CSV file. Please upload a correctly formatted CSV.")
        st.stop()


    # ========================================================
    # 3. Dataset Overview
    # ========================================================

    st.subheader("Dataset Preview & Metadata")

    # Display first 5 rows
    st.write("**First 5 Rows:**")
    st.dataframe(df.head())


    # --------------------------------------------------------
    # Display dimensional properties
    # --------------------------------------------------------

    st.write("**Dataset Dimensions:**")

    rows, columns = df.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Number of Rows", rows)

    with col2:
        st.metric("Number of Columns", columns)


    # --------------------------------------------------------
    # Display column data types
    # --------------------------------------------------------

    st.write("**Column Data Types:**")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(dtype_df)


    # --------------------------------------------------------
    # Missing value summary
    # --------------------------------------------------------

    st.write("**Missing Values per Column:**")

    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing Percentage": missing_percentage.round(2)
    })

    st.dataframe(missing_df)


    # --------------------------------------------------------
    # Basic statistics for numerical columns
    # --------------------------------------------------------

    st.write("**Basic Numerical Statistics:**")

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_columns) > 0:

        # Calculate required statistics
        statistics = pd.DataFrame({
            "Mean": df[numerical_columns].mean(),
            "Median": df[numerical_columns].median(),
            "Minimum": df[numerical_columns].min(),
            "Maximum": df[numerical_columns].max()
        })

        st.dataframe(statistics)

    else:
        st.info("No numerical columns are present in the dataset.")


    # ========================================================
    # 4. Attribute Selection
    # ========================================================

    st.sidebar.header("Attribute Selection")

    # Create a dropdown to select one column
    selected_column = st.sidebar.selectbox(
        "Select an attribute:",
        df.columns
    )


    # --------------------------------------------------------
    # Detect column type
    # --------------------------------------------------------

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        column_type = "Numerical"
    else:
        column_type = "Categorical"


    # Display detected type
    st.sidebar.write(
        f"**Attribute Type:** {column_type}"
    )


    # ========================================================
    # 5. Visualization Rendering
    # ========================================================

    st.subheader("Visualization")


    # ========================================================
    # Numerical Attribute
    # ========================================================

    if column_type == "Numerical":

        st.write(
            f"Distribution of **{selected_column}**"
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        sns.histplot(
            data=df,
            x=selected_column,
            kde=True,
            ax=ax
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        ax.set_title(
            f"Distribution of {selected_column}"
        )

        st.pyplot(fig)

        plt.close(fig)


    # ========================================================
    # Categorical Attribute
    # ========================================================

    else:

        st.write(
            f"Frequency of **{selected_column}**"
        )

        # Count unique values
        counts = df[selected_column].value_counts(dropna=False)

        # Convert missing values to readable text
        counts.index = counts.index.astype(str)

        fig, ax = plt.subplots(figsize=(10, 5))

        sns.barplot(
            x=counts.index,
            y=counts.values,
            ax=ax
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        ax.set_title(
            f"Frequency Distribution of {selected_column}"
        )

        # Rotate labels if necessary
        plt.xticks(rotation=45)

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# No file uploaded
# ============================================================

else:

    st.info(
        "Please upload a CSV file to start EDA."
    )