import streamlit as st
import pandas as pd

# Initialize book data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Title", "Author", "Genre", "Year", "Status"])

# Load existing data or initialize
if "library_data" not in st.session_state:
    st.session_state.library_data = load_data()

# Application title
st.title("📚 Automatic Library Management System")
menu=st.sidebar.radio("menu", ["add book","view book","search books", "check out/return book"])
if menu=="add book":
   st.header("Add a new book to the library")
   with st.form("add_book_form"):
     title=st.text_input("Book title")
     author=st.text_input("author")
     genre=st.selectbox("genre",["fiction","non-fiction","science","biography","other"])
     year= st.number_input("Year of Publication", min_value=1000, max_value=2100, step=1, value=2023)
     submit= st.form_submit_button("Add Book")

   if submit:
     if title and author:
        new_book={"Title": title, "Author": author, "Genre": genre, "Year": year, "Status": "Available"}
        st.session_state.library_data = pd.concat([st.session_state.library_data, pd. DataFrame ([new_book])], ignore_index=True)
        st.success("Book added successfully!")
     else:
        st.error("Please fill in both Title and Author.")
#view all books
elif menu == "view books":
  st.header("Library Books")
  st.dataframe(st.session_state.library_data)

#search for a book
elif menu== "search books":
  st.header("Search for Books")
  search_option = st.radio("Search by", ["title", "Author"])
  query = st.text_input("Enter {search_option}:")

  if query:
    filtered_data=st.session_state.library_data[
    st.session_state.library_data[search_option].str.contains( query, case=False, na=False)
    ]
    if not filtered_data.empty:
      st.dataframe (filtered_data)
    else:
      st.warning(f"No books found matching {search_option}: {query}")

#Check out/return a book
elif menu== "check out/return book":
   st.header("Manage Book Status")
   with st.form("manage_status_form"):
     book_title = st.text_input("Enter Book Title")
     action =st.selectbox("Action", ["Check Out", "Return"])
     submit= st.form_submit_button("Update Status")
   if submit:
     if book_title:
       book_index = st.session_state.library_data[
        st.session_state.library_data["Title"].str.contains(book_title, case=False, na=False)
       ].index
       if not book_index.empty:
        current_status = st.session_state.library_data.loc[book_index[0], "Status"]
        if action == "Check Out" and current_status == "Available":
          st.session_state.library_data.at [book_index[8], "Status"] = "Checked Out"
          st.success("Book checked out successfully!")
        elif action == "Return" and current_status == "Checked Out":
          st.session_state.library_data.at[book_index[8], "Status"] = "Available"
          st.success("Book returned successfully!")
        else:
          st.error(f"Cannot perform action. Current status: {current_status}")
       else:
          st.error("Book not found. Please check the title and try again.")
   else:
     st.error("Please enter a book title.")

