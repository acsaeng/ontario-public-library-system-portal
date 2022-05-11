# Ontario Public Library System Portal

**Authors:** Timothy Mok and Aron Saengchan

## Summary
This project focuses on a data set of statistics for the Ontario Public Library System from 2017 to 2019, made available by the Government of Canada [1]. Approximately 380 libraries self-report the data, providing general information such as the library names, codes, and addresses, as well as specific statistics on the number of cardholders and the number of English and French resources available at each branch. The project incorporates these data sets (using NumPy, Pandas, and Matplotlib) into an interactive portal for users to use as part of the Ontario Public Library System.

The program opens to a `Main Menu` where the user has four options to choose from:

1. **Branch Information Search** – The user is prompted to enter a library name or code and the program will provide them with specific information, including the address, website, and number of print/electronic resources available at that branch.
2. **Library Locator** – The user is prompted to enter a postal code and the program searches for any nearby libraries, while also considering the user’s needs. If any nearby branches are found, the program prints a list of them and allows the user to obtain information about a specific branch.
3. **Access Yearly Archives** – The user is prompted to enter a year between 2017 to 2019 and the program displays various statistical information from that year, from statistics of all library branches in the system to specific record-holders of each column in the data set.
4. **Quit** – Exits the program.

After each action, the user can perform the previous action again or return to the `Main Menu`. To start the program, open `opl_system_portal.py` and run the file.

## References 
1. Ontario public library statistics, Government of Canada, Jan. 2020. [Online]. Available: https://open.canada.ca/data/en/dataset/363fff31-6a07-41eb-9922-e9b64192b08

*This project was completed as part of ENSF 592: Programming Fundamentals for Data Engineers at the University of Calgary.*