import streamlit as st
import pandas as pd

# Processing Functions
def load_data(file):
    """Load the uploaded file into a DataFrame, considering the pipe delimiter."""
    return pd.read_csv(file, delimiter='|', dtype=str)

def shuffle_data(df):
    """Shuffle the DataFrame rows."""
    return df.sample(frac=1).reset_index(drop=True)

def drop_customer_id(df):
    """Drop the 'CUSTOMER_ID' column from the DataFrame."""
    return df.drop(columns=["CUSTOMER_ID"], errors="ignore")

def remove_duplicates(df):
    """Remove duplicate entries based on 'MSISDN'."""
    initial_count = len(df)
    df = df.drop_duplicates(subset="MSISDN", keep="first")
    removed_count = initial_count - len(df)
    return df, removed_count

def validate_msisdn(df):
    """Keep only valid 'MSISDN' entries."""
    return df[df["MSISDN"].astype(str).str.match(r'3[0-9]{9}$')]

def split_data(df, split_percentage):
    """Split the DataFrame based on a specified percentage."""
    split_point = int(len(df) * (split_percentage / 100))
    return df[:split_point], df[split_point:]

# Streamlit UI
st.sidebar.header("Upload & Settings")
uploaded_file = st.sidebar.file_uploader("Choose a file (TXT or CSV)", type=['txt', 'csv'])
output_file_name = st.sidebar.text_input("Output CSV name", "output.csv")
split_option = st.sidebar.checkbox("Split file into two?")
if split_option:
    split_percentage = st.sidebar.slider("Split Percentage", min_value=0, max_value=100, value=60, step=10)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.write("Preview of Uploaded File:", df.head(10))

    if st.button("Shuffle List"):
        df = shuffle_data(df)
        st.success("List shuffled successfully.")
        st.write("Shuffled List:", df.head(10))

    df = drop_customer_id(df)
    df, removed_count = remove_duplicates(validate_msisdn(df))
    if removed_count > 0:
        st.success(f"Removed {removed_count} duplicate MSISDN entries.")
    else:
        st.info("No duplicate MSISDN entries found.")

    if split_option:
        df1, df2 = split_data(df, split_percentage)
        st.write(f"First {split_percentage}% of Data:", df1.head(10))
        st.write(f"Remaining {100 - split_percentage}% of Data:", df2.head(10))

        # Download buttons for split files
        st.download_button("Download First Part", df1.to_csv(index=False), file_name=f"first_part_{output_file_name}")
        st.download_button("Download Second Part", df2.to_csv(index=False), file_name=f"second_part_{output_file_name}")
    else:
        # Download button for the processed file
        st.download_button("Download Processed CSV", df.to_csv(index=False), file_name=output_file_name)
else:
    st.info("Please upload a file to get started.")
