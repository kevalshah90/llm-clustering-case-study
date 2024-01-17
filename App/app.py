import streamlit as st
import pandas as pd 

def main():
    st.title("S&P500 Company Clutering")
    st.write("A Streamlit app using a pandas DataFrame for company clustering.")

    empty_df = pd.DataFrame({})
    
    # Load DataFrame
    df = pd.read_csv("df_cik_final.csv")

    # Create a dropdown for filtering
    selection = st.sidebar.selectbox("Company select", list(df.company_name.unique()))

    # get the cluster #
    mask = df['company_name'] == selection
    val = df.loc[mask, 'cluster'].item()
    
    # Apply the filter if a value is provided
    if selection:
        dff = df[df["cluster"] == val]
        df_filtered = dff[['cik','company_name','summary']]
    else:
        df_filtered = empty_df

    # Display the filtered DataFrame
    st.dataframe(df_filtered)

if __name__ == '__main__':
    main()
