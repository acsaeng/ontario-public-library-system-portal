from typing import Type
import numpy as np
import pandas as pd


class LibraryPortal:
    """A class used to represent an interactive library portal

        Attributes:
            data (DataFrame): DataFrame that stores detailed information about each library branch

        Methods:
            branch_search(): Return information about a specific library branch
            method2(): Description
            method3(): Description
    """
    def __init__(self, data):
        self.data = data
    
    def branch_search(self):
        while True:
            library_id = input("Please enter a library branch name or code: ")
            idx = pd.IndexSlice

            try:
                if library_id in self.data.index.get_level_values('Library Full Name'):
                    branch_df = self.data.loc[idx[library_id, :, :], idx[:]]
                    branch_series = branch_df.iloc[-1]
                    break
                elif library_id in self.data.index.get_level_values('Library Number'):
                    branch_df = self.data.loc[idx[:, library_id, :], idx[:]]
                    branch_series = branch_df.iloc[-1]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid library name or code. Please enter again.")


        print("\n***LIBRARY BRANCH INFORMATION***")

        branch_dict = {"Library Name": branch_df.index[-1][0],
                        "Library Number": branch_df.index[-1][1],
                        "Service Region" : branch_series['Ontario Library Service Region'],
                        "Street Address": [branch_series['Street Address'], branch_series['City/Town'], branch_series['Postal Code']],
                        "Website": branch_series['Web Site Address'],
                        "Number of Print Resources": branch_series['Total Print Titles Held'],
                        "Number of e-Book/e-Audio Resources": branch_series['Total E-book and E-audio Titles']
                        }
        
        for header, info in branch_dict.items():
            if info is np.nan:
                print(header + ": N/A")
            elif header == "Street Address":
                try:
                    print(header + ": " + info[0] + "\n\t\t" + info[1] + ", ON, " + info[2])
                except TypeError:
                    print(header + ": N/A")
            else:
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
    # data['Resources per Cardholder'] = data['Total Resources'] / data['No. Cardholders']
    # data.to_excel(r'Test.xlsx', index=True)

    return data


def main():
    # Import complete library data and create a LibraryPortal object
    library_data = add_data(import_data())
    portal = LibraryPortal(library_data)

    while True:
        print("\n***MAIN MENU***")
        print("1. Branch Information Search")
        print("2. Libraries Near Me")
        print("3. Yearly Archives")
        print("4. Quit")

        # Prompt user selection
        while True:
            # Verify that input is a valid numbered option from above
            try:
                user_selection = int(input("\nPlease select an action: "))

                if user_selection in range(1, 5):
                    break
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input in invalid
                print("Invalid input! Please enter a number between 1 and 4.")
        
        if user_selection == 1:
            # Option 1: Branch Information Search
            # A tool to find more information about a specific library branch
            portal.branch_search()
        elif user_selection == 2:
            pass
        elif user_selection == 3:
            pass
        elif user_selection == 4:
            print("Thank you for using the Ontario Public Library System Portal!")
            break


if __name__ == '__main__':
    main()

