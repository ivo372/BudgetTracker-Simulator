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