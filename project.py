from typing import Type
import numpy as np
import pandas as pd


class LibraryPortal:
    """A class used to represent an interactive library portal

        Attributes:
            data (DataFrame): DataFrame that stores detailed information about each library branch

        Methods:
            main_menu():
            branch_search(): Search the data for information of a specific library branch
            method2(): Description
            method3(): Description
            print_branch_data(): Print the information of a specific library branch
    """
    def __init__(self, data):
        self.data = data
    
    def main_menu(self):
        """
        """
        print("\n***MAIN MENU***")
        print("1. Branch Information Search")
        print("2. Libraries Locator")
        print("3. Resource Archives")
        print("4. Quit")

        # Prompt user selection
        while True:
            # Verify that input is a valid numbered option from above
            try:
                user_selection = int(input("\nPlease select an action: "))

                if user_selection == 1:
                    # Option 1: Branch Information Search
                    # A tool to find more information about a specific library branch
                    self.branch_search()
                    self.main_menu()
                elif user_selection == 2:
                    break
                elif user_selection == 3:
                    break
                elif user_selection == 4:
                    print("Thank you for using the Ontario Public Library System Portal!")
                    exit()
                else:
                        raise ValueError
            except ValueError:
                # Raise ValueError if input in invalid
                print("Invalid input! Please enter a number between 1 and 4.")

    def branch_search(self):
        idx = pd.IndexSlice

        while True:
            library_id = input("Please enter a library branch name or code: ")

            try:
                if library_id in self.data.index.get_level_values('Library Full Name'):
                    branch_data = self.data.loc[idx[library_id, :, :], idx[:]]
                    break
                elif library_id in self.data.index.get_level_values('Library Number'):
                    branch_data = self.data.loc[idx[:, library_id, :], idx[:]]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid library name or code. Please enter again.")

        self.print_branch_info(branch_data)

        while True:
            print("\nEnter [m] to go to the Main Menu")
            user_action = input("Enter [b] to go back and search again: ")

            try:
                if user_action == "b":
                    self.branch_search()
                elif user_action == 'm':
                    self.main_menu()
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter again.")


    def print_branch_info(self, branch_df):
        branch_series = branch_df.iloc[-1]

        branch_dict = {"Library Name": branch_df.index[-1][0],
                        "Library Number": branch_df.index[-1][1],
                        "Service Region" : branch_series['Ontario Library Service Region'],
                        "Street Address": None,
                        "Website": branch_series['Web Site Address'],
                        "Number of Print Resources": branch_series['Total Print Titles Held'],
                        "Number of e-Book/e-Audio Resources": branch_series['Total E-book and E-audio Titles']
                        }

        try:
            branch_dict["Street Address"] = branch_series['Street Address'] + "\n\t\t" + branch_series['City/Town'] + ", ON, " + branch_series['Postal Code']
        except TypeError:
            branch_dict["Street Address"] = np.nan

        print("\n***LIBRARY BRANCH INFORMATION***")

        # Interate through branch dictionary to print its information in a readable format
        for header, info in branch_dict.items():
            if info is np.nan:
                # If dataset value is NaN, print "N/A" for the field
                print(header + ": N/A")
            else:
                # Otherwise, print the value in the dataset
                print(header + ": " + str(info))


def import_data():
    library_data_2017 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2017.xlsx", index_col=[0, 1, 2])
    library_data_2018 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2018.xlsx", index_col=[0, 1, 2])
    library_data_2019 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2019.xlsx", index_col=[0, 1, 2])

    library_data_master = pd.concat([library_data_2017, library_data_2018, library_data_2019])
    library_data_master = library_data_master.sort_index()

    return library_data_master


def add_data(data):
    data['Total Resources'] = data['Total Print Titles Held'] + data['Total E-book and E-audio Titles']
    
    data['No. Cardholders'].replace(0, np.nan, inplace=True)
    data['Resources per Cardholder'] = data['Total Resources'] / data['No. Cardholders']
    data.to_excel(r'Test.xlsx', index=True)

    return data


def main():
    # Import complete library data from excel files
    library_data = add_data(import_data())
    
    # Create a LibraryPortal object and access the main menu
    portal = LibraryPortal(library_data)
    portal.main_menu()

if __name__ == '__main__':
    main()