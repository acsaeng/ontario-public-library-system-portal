import numpy as np
import pandas as pd


class LibraryPortal:
    """A class used to represent an interactive library portal

        Attributes:
            data (DataFrame): DataFrame that stores detailed information about each library branch

        Methods:
            library_lookup(): Return information about a specific library branch
            method2(): Description
            method3(): Description
    """

    def __init__(self, data):
        self.data = data
    
    def library_lookup(self):
        while True:
            library_id = input("Please enter a library branch name or code: ")
            idx = pd.IndexSlice

            try:
                if library_id in self.data.index.get_level_values('Library Full Name'):
                    branch_data = self.data.loc[idx[library_id, :, 2019], idx[:]]
                    break
                elif int(library_id) in self.data.index.get_level_values('Library Number'):
                    branch_data = self.data.loc[idx[:, library_id, 2019], idx[:]]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid library name or code. Please enter again.")

        print("***Library Branch Information***")
        print("Library Name: " + branch_data.index.get_level_values('Library Full Name')[0])
        print("Library Number: " + branch_data.index.get_level_values('Library Number')[1])
        print("Service Region: ")
        print("\nStreet Address: ")
        print("Website: ")
        print("Number of Print Resources: ")
        print("Number of e-Book/e-Audio Resources: ")






def import_data():
    library_data_2017 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2017.xlsx", index_col=[0, 1, 2])
    library_data_2018 = pd.read_csv(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2018.csv", index_col=[0, 1, 2])
    library_data_2019 = pd.read_csv(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2019.csv", index_col=[0, 1, 2])

    library_data_master = pd.concat([library_data_2017, library_data_2018, library_data_2019])
    library_data_master = library_data_master.sort_index()

    return library_data_master

    # library_master_data.to_excel(r'Test.xlsx', index=True)

def add_data(data):
    data['Total Resources'] = data['Total Print Titles Held'] + data['Total E-book and E-audio Titles']
    
    data['No. Cardholders'].replace(0, np.nan, inplace=True)
    # data['Resources per Cardholder'] = data['Total Resources'] / data['No. Cardholders']
    data.to_excel(r'Test.xlsx', index=True)
    print(data)

    return data


def main():
    # Import complete library data and create a LibraryPortal object
    library_data = add_data(import_data())
    portal = LibraryPortal(library_data)

    # Prompt user selection
    while True:
        print("1. Library lookup")
        print("2. Find a library near you")
        print("3. Archives")
        print("4. Quit")

        # Verify that input is a valid numbered option from above
        try:
            user_selection = int(input("\nPlease select an action: "))
            
            if user_selection == 1:
                # Option 1: Library Lookup
                # A tool to find more information about a specific library branch
                portal.library_lookup()
            elif user_selection == 2:
                pass
            elif user_selection == 3:
                pass
            elif user_selection == 4:
                print("Thank you for using the Ontario Public Library System Portal!")
                break
            else:
                raise ValueError
        except ValueError:
            # Raise ValueError if an option is not selected
            print("Invalid input! Please enter a number between 1 and 4.")


if __name__ == '__main__':
    main()

