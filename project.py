# ENSF 592 Project
# project.py
#
# Timothy Mok & Aron Saengchan
# Group 30 
#
# A terminal based application that serves as an interactive portal for the Ontario Public Library System. The library
# portal object in this program contains public library data from 2017 to 2019 and options that users can perform to navigate 
# this data. The user has the choice to select from one of four options from the Main Menu - Branch Information Search, 
# Library Locator, Access Yearly Archives, and Quit - and can go back and forth between these actions within the interface.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


class LibraryPortal:
    """A class used to represent an interactive library portal interface

        Attributes:
            data (DataFrame): DataFrame that stores detailed information about each library branch

        Methods:
            main_menu(): Prompt user to select an option in the library portal
            next_user_action(current_option, *opt_nearby_branches): Prompt user to go back to the Main Menu or repeat the current action
            branch_search(): Search the data for information about a specific library branch
            print_branch_info(branch_df): Print the information of a specific library branch
            library_locator(): Find a library branch nearby based on user's postal code and needs
            print_nearby_branches(sorted_locations): Print a list of nearby library branches
            access_archive(): Access yearly data and statistical information of the library system
            generate_plots(year): Generate two plots and output it to the user 
    """
    def __init__(self, data):
        self.__data = data
    
    def main_menu(self):
        """Main menu that display a list of options on the library portal and prompts the user to select one

            Parameters:
                None
            
            Returns:
                None
        """
        print("\n==========| MAIN MENU |==========\n")
        print("1. Branch Information Search")
        print("2. Library Locator")
        print("3. Access Yearly Archives")
        print("4. Quit")

        # Prompt user to select an option
        while True:
            # Verify that input is a valid numbered option from above
            try:
                user_selection = int(input("\nPlease select an option: "))

                if user_selection == 1:
                    # Option 1: Branch Information Search
                    # A tool to find information about a specific library branch
                    self.branch_search()
                elif user_selection == 2:
                    # Option 2: Library Locator
                    # A tool to find a suitable library branch near you
                    self.library_locator()
                elif user_selection == 3:
                    # Option 3: Access Yearly Archives
                    # A tool to view yearly data and statistics of the library system
                    self.access_archives()
                elif user_selection == 4:
                    # Option 4: Quit
                    # Exit the Ontario Public Library System Portal
                    print("\nThank you for using the Ontario Public Library System Portal!")
                    exit()
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input is invalid
                print("Invalid input. Please enter a number between 1 and 4.")

    def next_user_action(self, current_option, *opt_nearby_branches):
        """Prompt for user to choose whether to go to the Main Menu or go back to perform the current option again

            Parameters:
                current_option (int or float): A number that signifies what option the user is currently performing
                *opt_nearby_branches (list): A list that contains a DataFrame of nearby library branches if user wants to print them again

            Returns:
                None
        """
        # Prompt user to select an option
        while True:
            print("\nEnter [m] to go to the Main Menu")
            next_action = input("Enter [b] to go back: ")

            try:
                if next_action == "m":
                    # If user enters 'm', go back to the main menu. 
                    self.main_menu()
                elif next_action == "b" and current_option == 1:
                    # If user enters 'b' for any of the options below, perform previous action
                    self.branch_search()
                elif next_action == "b" and current_option == 2.1:
                    self.library_locator()
                elif next_action == "b" and current_option == 2.2:
                    self.print_nearby_branches(opt_nearby_branches[-1])
                elif next_action == "b" and current_option == 3:
                    self.access_archives()
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input is invalid
                print("Invalid input. Please enter again.")

    def branch_search(self):
        """Search for the information of a user-specified library branch using its name or code

            Parameters:
                None

            Returns:
                None
        """
        print("\n==========| BRANCH INFORMATION SEARCH |==========\n")

        # Prompt user input for library branch name or code
        while True:
            library_id = input('Please enter a library branch name or code (e.g. "Toronto" or "L0353"): ').title()

            try:
                # If input is valid, use an index slice on the DataFrame to obtain the information of the selected library branch
                if library_id in self.__data.index.get_level_values('Library Full Name'):
                    # Continue if "Library Full Name" input is valid
                    branch_data = self.__data.loc[pd.IndexSlice[library_id, :, :], pd.IndexSlice[:]]
                    break
                elif library_id in self.__data.index.get_level_values('Library Number'):
                    # Continue if "Library Number" input is valid
                    branch_data = self.__data.loc[pd.IndexSlice[:, library_id, :], pd.IndexSlice[:]]
                    break
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input is invalid
                print("Invalid library name or code. Please enter again.")

        self.print_branch_info(branch_data)  # Print the information of the selected library branch
        self.next_user_action(1)  # Prompt user to select next action

    def print_branch_info(self, branch_df):
        """Display the information of a selected library branch to the user on the console

            Parameters:
                branch_df (DataFrame): DataFrame containing all the data of a specific library branch

            Returns:
                None 
        """
        branch_series = branch_df.iloc[-1]  # Slice the data of the most recent year (2019) from the DataFrame

        # Create a dictionary to map the keys to their correct value counterparts in the DataFrame columns using the proper indices
        branch_dict = {"Library Name": branch_df.index[-1][0],
                        "Library Number": branch_df.index[-1][1],
                        "Service Region": branch_series['Ontario Library Service Region'],
                        "Street Address": None,  # Initialized as 'None' to properly format the address below
                        "Website or E-mail": branch_series['Web Site Address'],
                        "Number of Print Resources": branch_series['Total Print Titles Held'],
                        "Number of e-Book/e-Audio Resources": branch_series['Total E-book and E-audio Titles']}

        try:
            # Try formatting selected elements to generate a proper street address of the library branch
            branch_dict['Street Address'] = branch_series['Street Address'] + "\n\t\t" + branch_series['City/Town'] + ", ON, " + branch_series['Postal Code']
        except TypeError:
            # If data is missing in any of the elements, assign the 'Street Address' key with a NaN value
            branch_dict["Street Address"] = np.nan

        print("\n*****LIBRARY BRANCH INFORMATION*****\n")

        # Iterate through branch dictionary to print its information in a readable format
        for header, info in branch_dict.items():
            if info is np.nan:
                # If dataset value is NaN, print "N/A" in its field
                print(header + ": N/A")
            else:
                # Otherwise, print the value in the dictionary
                print(header + ": " + str(info))

    def library_locator(self):
        """Find library branch locations near the user based on their postal code and needs

            Parameters:
                None
            
            Returns:
                None
        """
        print("\n==========| LIBRARY LOCATOR |==========\n")

        # Prompt user to input a postal code
        while True:
            postal_code = input("Please enter a postal code (K1A1A1): ")

            try:
                # Check if postal code is valid (i.e. contains six alternating alphanumeric characters) using regex
                if len(postal_code) == 6 and re.compile(r'([a-zA-Z][0-9]){3}').match(postal_code):
                    postal_code = postal_code.upper()  # Convert letters to uppercase if any are lowercase
                    break
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input is invalid
                print("Please enter a valid postal code.")

        # Use a boolean mask to filter the postal codes of the library branches that match the first three characters of the user's postal code
        data_by_postal_code = self.__data.loc[pd.IndexSlice[:, :, 2019], pd.IndexSlice[:]][self.__data.loc[pd.IndexSlice[:, :, 2019], pd.IndexSlice['Postal Code']].str.match(r'^' + postal_code[:3])]

        if len(data_by_postal_code.index) == 0:
            # If filtered DataFrame is empty, print message to user that no libraries were found 
            print("\nSorry! Could not find any libraries nearby.")
            self.next_user_action(2.1)  # Prompt user to select next action

        else:
            # Otherwise, sort the nearby library branches based on the user's needs
            print("\nWhat are you looking for today?")
            print("1. Borrow Library Resources")
            print("2. Work or Study Spaces")
            print("3. No Preference")
            
            # Prompt user to select an option
            while True:
                # Verify that input is a valid numbered option from above
                try:
                    user_selection = int(input("\nPlease select an option: "))

                    # Depending on the user's needs, sort the filtered DataFrame accordingly
                    if user_selection == 1:
                        # If user wants to borrow library resources, sort by highest "Resources per Cardholder"
                        data_by_postal_code = data_by_postal_code.sort_values('Resources per Cardholder', ascending=False)
                        break
                    elif user_selection == 2:
                        # If user wants a study or work space, sort by lowest "No. Cardholders"
                        data_by_postal_code = data_by_postal_code.sort_values('No. Cardholders')
                        break
                    elif user_selection == 3:
                        # If user has no preference, randomize the filtered DataFrame
                        data_by_postal_code = data_by_postal_code.sample(frac=1)
                        break
                    else:
                        raise ValueError
                except ValueError:
                    # Raise ValueError if input is invalid
                    print("Invalid input. Please enter a number between 1 and 3.")
        
            self.print_nearby_branches(data_by_postal_code)  # Print the nearby library branches
                
    def print_nearby_branches(self, sorted_locations):
        """Print a list of nearby library locations and lets the user obtain information from any of them

            Parameters:
                sorted_locations (DataFrame): A filtered and sorted DataFrame containing a list of nearby library branches
            
            Returns:
                None
        """
        # Print the first five library branches nearby and available to the user
        print("\nHere is a list of libraries we found for you:")

        for i, row_index in enumerate(sorted_locations.iterrows(), start=1):
            print(str(i) + ". " + row_index[0][0])
        
            if i == 5:
                break
        
        # Prompt user to select a library branch from the list
        while True:
            try:
                branch_selection = int(input("\nSelect a number to view its branch information: "))

                if branch_selection in range(1, 6):
                    # If valid number, obtain the library name
                    branch_name = sorted_locations.index.get_level_values('Library Full Name')[branch_selection - 1]
                    break
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input is invalid
                print("Invalid input. Please enter a number between 1 and 5.")

        # Use the library name to slice its data from the original DataFrame
        self.print_branch_info(self.__data.loc[pd.IndexSlice[branch_name, :, :], pd.IndexSlice[:]])
        self.next_user_action(2.2, sorted_locations)  # Prompt user to select next action

    def access_archives(self):
        """Access yearly archives displaying various data and statistical information of the Ontario Public Library System

            Parameters:
                None

            Returns:
                None 
        """
        print("\n==========| ACCESS LIBRARY ARCHIVES |==========\n")

        # Prompt user to enter a year between 2017 and 2019
        while True:
            try:
                year = int(input("Please enter a year between 2017 and 2019: "))

                if year in range(2017, 2020):
                    # If year is valid, break and print the archived data from that year
                    break
                else:
                    raise ValueError
            except ValueError:
                # Raise ValueError if input is invalid
                print("Invalid archive year. Please enter again.")

        print("\n*******LIBRARY STATISTICAL ARCHIVES IN " + str(year) + "*******")

        # Create a row that aggregates the sum of all columns in the DataFrame
        sum_row = self.__data.groupby('Year').sum().loc[year, :]
        sum_row.rename('sum', inplace=True)
        sum_df = pd.DataFrame(sum_row)
       
        # Concatenate the summed row to a set of described data statistics and print the DataFrame
        print("\n*****GENERAL DATA STATISTICS*****\n")
        described_data = pd.concat([self.__data.loc[pd.IndexSlice[:, :, year], pd.IndexSlice[:]].describe(), sum_df.T])
        print(described_data)

        # Create and print a pivot table containing the average 'Resources per Cardholder' by 'Service Region' and 'Service Type'
        print("\n*****AVERAGE RESOURCES PER CARDHOLDER BY SERVICE REGION & TYPE*****\n")
        service_type_pivot = self.__data.pivot_table('Resources per Cardholder', index='Service Type', columns='Ontario Library Service Region')
        service_type_pivot.replace(0, "0.0*", inplace=True)  # Add annotations to null values for the side notes below
        service_type_pivot.replace(np.nan, "N/A**", inplace=True)  # Add annotations to NaN values for the side notes below
        print(service_type_pivot)
        
        # Display side notes pertaining to the null or NaN values in the above pivot table
        print("\nNotes:")
        print("  *0.0 may indicate missing data for some library branches")
        print("  **N/A denotes that the service type is not offered in the corresponding region")

        print("\n*****LIBRARY RECORDS*****\n")
        # Print the libraries with the max values in each column, serving as the library record-holders
        for col in self.__data.columns[8:]:
            max_value = self.__data.loc[pd.IndexSlice[:, :, year], pd.IndexSlice[col]].max()
            branch_name = self.__data[self.__data[col] == max_value].index[0][0]
            print("Most " + col + ": " + branch_name + " (" + str(max_value) + ")")

        # Generate and display the Matplotlib plots
        print("\nPlease close the plots to continue...")
        self.generate_plots(year)
    
        self.next_user_action(3)  # Prompt user to select next action

    def generate_plots(self, year):
        """Generate a line and a bar plot that illustrates a comparison of the number of prints and e-resources by language and year

            Parameters:
                year (int): A specified year that dictates the data the first plot will display

            Returns:
                None
        """
        # Slice the sum of the total number of print titles and e-resources data from the DataFrame
        print_titles_data = self.__data.groupby('Year').sum().loc[pd.IndexSlice[:], pd.IndexSlice['English Print Titles Held':'Other Print Titles Held']]
        eresources_data = self.__data.groupby('Year').sum().loc[pd.IndexSlice[:], pd.IndexSlice['English E-book and E-audio Titles':'Other E-book and E-audio Titles']]

        # Create and format a plot showing the total number of resources by language and type in the specified year
        plt.figure(1)
        plt.bar([0, 0.75, 1.5], print_titles_data.loc[year], width=0.2)
        plt.bar([0.2, 0.95, 1.7], eresources_data.loc[year], width=0.2)
        plt.title('Total Number of Resources by Language and Resource Type in ' + str(year))
        plt.xlabel('Language')
        plt.xticks([0.1, 0.85, 1.6], ['English', 'French', 'Other'])
        plt.ylabel('Number of Resources')
        plt.legend(['Print Titles', 'E-book and E-audio Titles'], loc='upper right')

        # Merge the previous data into two other separate DataFrames categorized by language
        english_resources = pd.merge(print_titles_data['English Print Titles Held'], eresources_data['English E-book and E-audio Titles'], on='Year')
        french_resources = pd.merge(print_titles_data['French Print Titles Held'], eresources_data['French E-book and E-audio Titles'], on='Year')

        # Create a plot containing two sub-plots showing the yearly trend of the total number of resources by language and type
        subplot = plt.figure(2)
        (top, bottom) = subplot.subplots(2)
        subplot.suptitle('Trend of Total Number of Resources by Language and Type (2017-2019)')
        top.plot(english_resources)
        bottom.plot(french_resources)
        top.set(title='English Resources', xlabel='Year', xticks=[2017, 2018, 2019], ylabel='Number of English Resources', ylim=[10000000, 30000000]) 
        bottom.set(title='French Resources', xlabel='Year', xticks=[2017, 2018, 2019], ylabel='Number of French Resources', ylim=[200000, 1300000])
        top.legend(['Print Titles ', 'E-book and E-audio Titles'], loc='upper right')
        bottom.legend(['Print Titles ', 'E-book and E-audio Titles'], loc='upper right')
        
        plt.show()  # Show the plots in a new window


def import_data():
    """Import all the Ontario Public Library data sets from the working directory and merge them together

        Parameters:
            None
        
        Returns:
            DataFrame that stores detailed information about each library branch
    """
    # Import the Ontario Public Library System Excel data sets from 2017 to 2019 
    library_data_2017 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2017.xlsx")
    library_data_2018 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2018.xlsx")
    library_data_2019 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2019.xlsx")

    # Merge all the data sets together on all of their columns
    library_data_merge = pd.merge(library_data_2017, library_data_2018, on=list(library_data_2019.columns), how='outer')
    library_data_master = pd.merge(library_data_merge, library_data_2019, on=list(library_data_2019.columns), how='outer')

    # Forward fill the missing 'Street Address' columns with valid 'Mailing Address' columns
    library_data_master[['Mailing Address', 'Street Address']] = library_data_master[['Mailing Address', 'Street Address']].fillna(method='ffill', axis=1)

    # Sort the indices to obtain an organized DataFrame with hierarchical indices
    library_data_master = library_data_master.set_index(['Library Full Name', 'Library Number', 'Year']).sort_index()

    return library_data_master


def add_columns(library_data):
    """Create two additional columns and add them to the Dataframe

        Parameters:
            library_data (DataFrame): DataFrame that stores detailed information about each library branch

        Returns:
            The original DataFrame with two added columns ('Total Print Titles Held' and 'Resources per Cardholder')

    """
    # Create two columns of the total print titles held and resource available per cardholder, and add it to the DataFrame
    library_data['Total Resources'] = library_data['Total Print Titles Held'] + library_data['Total E-book and E-audio Titles']
    library_data['Resources per Cardholder'] = library_data['Total Resources'] / library_data['No. Cardholders']
    
    # Replace all the NaN values with 0 as a result of dividing by zero from missing data 
    library_data['Resources per Cardholder'].replace(np.nan, 0, inplace=True)

    return library_data


def main():
    """Obtain the library data and create a LibraryPortal object to serve as an interactive portal for the Ontario Public Library System

        Parameters:
            None

        Returns:
            None
    """
    # Import and merge library data sets from Excel files and add new columns to it, 
    library_data = add_columns(import_data())

    # Export the merged, hierarchical dataset to an Excel file in the working directory (commented out)
    # library_data.to_excel(r'.\exported_library_statistics.xlsx', index=True)
    
    # Create a LibraryPortal object and access the Main Menu
    portal = LibraryPortal(library_data)
    portal.main_menu()


if __name__ == '__main__':
    main()