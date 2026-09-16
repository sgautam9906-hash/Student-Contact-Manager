import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Contact Manager",
    page_icon="📚"
)

st.title("📚 Student Contact Manager")

# Store students
if "students" not in st.session_state:
    st.session_state.students = []

# ================= ADD STUDENT =================

st.subheader("➕ Add Student")

student_id = st.text_input("Student ID", key="add_id")
name = st.text_input("Student Name", key="add_name")
contact = st.text_input("Contact Details", key="add_contact")

if st.button("Add Student"):

    if student_id and name and contact:

        existing_ids = [
            student["Student ID"]
            for student in st.session_state.students
        ]

        if student_id in existing_ids:
            st.error("Student ID already exists!")

        else:
            st.session_state.students.append({
                "Student ID": student_id,
                "Name": name,
                "Contact Details": contact
            })

            st.success("Student added successfully! 🎉")

    else:
        st.warning("Please fill in all the details.")

# ================= SEARCH =================

st.divider()

st.subheader("🔍 Search Students")

search = st.text_input(
    "Search by Student ID, Name or Contact",
    placeholder="Type here..."
)

# ================= DISPLAY =================

st.subheader("📋 Student Records")

if st.session_state.students:

    df = pd.DataFrame(st.session_state.students)

    if search:
        filtered_df = df[
            df.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]
    else:
        filtered_df = df

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.write(f"**Total Students:** {len(df)}")
    st.write(f"**Students Found:** {len(filtered_df)}")

else:
    st.info("No student records added yet.")

# ================= UPDATE =================

st.divider()

st.subheader("✏️ Update Student")

if st.session_state.students:

    student_ids = [
        student["Student ID"]
        for student in st.session_state.students
    ]

    selected_id = st.selectbox(
        "Select Student ID",
        student_ids
    )

    # Find selected student
    selected_student = next(
        student
        for student in st.session_state.students
        if student["Student ID"] == selected_id
    )

    new_id = st.text_input(
        "Student ID",
        value=selected_student["Student ID"],
        key="update_id"
    )

    new_name = st.text_input(
        "Student Name",
        value=selected_student["Name"],
        key="update_name"
    )

    new_contact = st.text_input(
        "Contact Details",
        value=selected_student["Contact Details"],
        key="update_contact"
    )

    if st.button("Update Student"):

        # Check if new ID is already used by another student
        duplicate = any(
            student["Student ID"] == new_id
            and student["Student ID"] != selected_id
            for student in st.session_state.students
        )

        if duplicate:
            st.error("Another student already has this ID.")

        elif new_id and new_name and new_contact:

            selected_student["Student ID"] = new_id
            selected_student["Name"] = new_name
            selected_student["Contact Details"] = new_contact

            st.success("Student updated successfully! ✅")

        else:
            st.warning("Please fill in all the details.")

# ================= DELETE =================

st.divider()

st.subheader("🗑️ Delete Student")

if st.session_state.students:

    delete_id = st.selectbox(
        "Select Student to Delete",
        [
            student["Student ID"]
            for student in st.session_state.students
        ],
        key="delete_student"
    )

    if st.button("Delete Student"):

        st.session_state.students = [
            student
            for student in st.session_state.students
            if student["Student ID"] != delete_id
        ]

        st.success("Student deleted successfully! 🗑️")