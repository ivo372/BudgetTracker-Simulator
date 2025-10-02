# Development Journal

# Day 0 - 23/09/2025
- Initialized the Budget Tracker project folder.

- Installed Python, virtual environment, and initial dependencies (pandas, tabulate, pytest).

- Planned the project structure: budget/, tests/, data/.

- Learned about Python packages and __init__.py .

# Day 1 - 24/09/2025

- Focused on file_handling.py functions: create_file, add_record, load_data, save_data.

- Implemented and ran tests with pytest using tmp_path.

- Learned about handling optional fields ("Note") and pandas FutureWarnings.

- Fixed import issues using editable install (pip install -e .).

- Ensured all tests pass and file handling works as intended.

# Day 2 - 26/09/2025

- Started on core_functions and so far developed: add_income, add_expense, view_all_records and calculate_total_expenses

- Decided to divide the functions into income and expense. Ex: min_income, min_expense, calculate_total_income,...

- Test the functions I developed today, covered normal scenarios only; edge cases deferred for later

- Opted for handling user input in the future, to have the code in core_functions clean

# Day 3 - 29/09/2025

- Finished developing and testing **Create** and **Read** functions:
    - Added **calculate_total_income** and upgraded **calculate_total_expenses**
    - Added **min/max/avg** functions for income and expenses
    - Category-based summaries
    - **print_report** tested with **capsys** 
- Separated tests into clear sections: **min/max/avg**, **add**, **total**, **category**, **view**, **print**
- Next steps: develop **Delete** and **Update** functions

# Day 4 - 30/09/2025

- Worked on the "Delete" functionality for the budget tracker.

- Implemented **delete_one_row** using row ID and **delete_all_rows** to clear the dataframe.

- Due to adding an ID column to the dataframe, had to make some updates in some previously tested functions.

- Decided not to include emptiness checks inside core functions, leaving that logic to the UX/main layer.

- Did not test today; Next Steps: fix tests and add "Update" functions

# Day 5 - 01/10/2025

- Implemented update functionalities: **update_record** and **update_type** in core functions.

- Added validation logic via **validate_record** to unify checks for date format, negative amounts, string types, and empty values.

- Integrated validation into **add_expense**, **add_income** and **update_record** functions to ensure data consistency.

- Core functions now fully cover CRUD operations with stable IDs and proper validation

- **Next Steps**:
    
    - Reorganize and consolidate tests to reflect updated validation and new functions.

    - Begin UX implementation

# Day 6 - 02/10/2025

- Strengthened file handling: ensured all columns exist, safe type coercion, auto-assigned IDs.

- Updated core functions and tests: defensive checks added for empty data, invalid input, negative amounts.

- Fixed issues: **view_all_records** ID dtype, min/max/avg calculations on empty DataFrames, **validate_record** rejecting invalid amounts.

- Ran full test suite – all 15 tests passed ✅

- Planned UX: structured main menu, input handling, and category report display (considering tabulate for tables).

- **Next Steps**:

    - Finish UX

    - Test UX