import csv
from datetime import datetime, timedelta
filename='Contacts.csv'
def contact_exister(Name,Number):#-----------------------------------------------------------------------CHECK DUPLICATE CONTACT
    try:
        with open(filename,'r')as file:
            reader=csv.reader(file)
            for row in reader:
              if row[0].lower()==Name.lower() or row[1]==Number:
                return True
    except FileNotFoundError:
        return False #for contact not found
    return False #for duplicate contact
def contact_adder():#------------------------------------------------------------------------------------------------ADD CONTACT
  while True:
    Name=input('Enter The Name To Add: ')
    Number=(input('Enter The Number To Add: '))
    if contact_exister(Name,Number):
      Choice=input('Contact already exists! do you still want to add it? (yes or no): ')
      if Choice.lower()=='yes':
        with open(filename,'a',newline='')as file:
          writer=csv.writer(file)
          writer.writerow([Name,Number])  
          print('Contact Saved successfully!') 
          print('\nDo you want to add another contact?')
          d=input('Yes or No: ')
          u=d.lower()
          if u!='yes':
            return
      elif Choice.lower()=='no':
        print('Contact not added!')
        return
      else:
        print('Invalid Input! please try again..')
        return
    else:
      with open(filename,'a',newline='')as file:
        writer=csv.writer(file)
        writer.writerow([Name,Number])  
        print('Contact Saved successfully!') 
        print('\nDo you want to add another contact?')
        d=input('Yes or No: ')
        u=d.lower()
        if u!='yes':
          return
def contact_viewer():#----------------------------------------------------------------------------------------------VIEW CONTACT
  try:
    with open(filename,'r')as file:
      file.seek(0)
      reader=csv.reader(file)
      print('\nContacts List')
      for row in reader:
        print(f'Name: {row[0]} | Number: {row[1]}')
      C=input("1. SEARCH CONTACT | 2. ADD CONTACT | 3. DELETE CONTACT | 4. EXIT: ")
      if C=='1':
        Contact_searcher()
      elif C=='2':
        contact_adder()
      elif C=='3':
        Contact_deleter()
      elif C=='4':
         return  
      else:
        print('Invalid Input! please try again..')
        return
  except FileNotFoundError:
    c=input('No contacts found! do you want to add contacts? (enter yes or no): ')
    if c.lower()=='yes':
      contact_adder()
    elif c.lower()=='no':
      return
    else:
      print("Invalid Input! please try again..")
      return  
def Contact_searcher():#-------------------------------------------------------------------------------------------SEARCH CONTACT
  key=input('Enter the name or number to search: ')
  found=False
  try:
    with open(filename,'r')as file:
      reader=csv.reader(file)
      for row in reader:
        if key.lower()in row[0].lower() or key in row[1]:
          print('\nContact Found!')
          print(f'Name: {row[0]} | Number: {row[1]}')
          found=True
    if not found:
      L=input('Contact not found! do you want to add it? (yes or no): ')
      if L.lower()=='yes':
        contact_adder()
      elif L.lower()=='no':
        return
      else:
        print('Invalid Input! please try again..')
        return 
  except FileNotFoundError:
    print('No contacts found!')
def Contact_deleter():#---------------------------------------------------------------------------------------------DELETE CONTACT
  K=int(input("1. DELETE CONTACT | 2. RECYCLE BIN: "))
  if(K==2):
     recycle_bin_viewer()
  elif(K==1):     
    KEY= input('Enter the name or number to delete: ')
    deleted=False
    try:
      with open(filename,'r')as file:
        reader=csv.reader(file)
        contacts=list(reader)
        new=[]
        delted=[]
        for row in contacts:
          if KEY.lower()==row[0].lower() or KEY==row[1]:
            l=input(f'Are you sure you want to delete (yes or no): ')
            if l.lower()=='yes':
              delted.append(row)
              deleted=True
            elif l.lower()=='no':
              return
            else:
              print('Invalid Input! please try again..')
              return
          else:
            new.append(row)
      if deleted:
        with open(filename,'w',newline='')as file:
          writer=csv.writer(file)
          writer.writerows(new)
        with open('recycle_bin.csv','a',newline='')as file:
          writer=csv.writer(file)
          for contact in delted:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([contact[0], contact[1], timestamp])
        print('Contact deleted successfully!')
        Q=input("Do you Want to delete another contact?(yes/no): ")
        if(Q.lower()!='yes'):
           return
      else:
        print('Contact not found!, please try again...')
    except FileNotFoundError:
      print('No contacts found!')
      return 
  else:
     print("Invalid Number! Please try again")
     return
def recycle_bin_emptier():#------------------------------------------------------------------------------RECYCLE BIN EMPTY 30 DAYS
  try:
    kept_contacts=[]
    with open('recycle_bin.csv','r',newline='')as file:
      reader=csv.reader(file)
      for row in reader:
        if(len(row))<3:
          continue
        try:
          deletion_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
          age = datetime.now() - deletion_date
          if age < timedelta(days=30):
            kept_contacts.append(row)
          else:
            print(f"Permanently deleting old contact from recycle bin: {row[0]}")
        except ValueError:
          kept_contacts.append(row)
      with open('recycle_bin.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(kept_contacts)
  except FileNotFoundError:
    return
  except Exception as e:
    print(f"An error occurred while cleaning the recycle bin: {e}")
def recycle_bin_viewer():#----------------------------------------------------------------------------------------RECYCLE BIN VIEW
    try:
        while True:
         with open("recycle_bin.csv", "r") as file:
             reader = csv.reader(file)
             rows = list(reader)
             if len(rows) == 0:
                 print("Recycle Bin is empty.")
                 return  # yahi se exit kar de
             print("Deleted Contacts in Recycle Bin:")
             for row in rows:
                 print(f"Name: {row[0]} | Number: {row[1]} | Deleted At: {row[2] if len(row) > 2 else 'N/A'}")        
         S = input("\n1. CONTACT RESTORE | 2. DELETE CONTACT PERMANENTLY(FORM RECYCLE BIN) | 3. EXIT : ").strip()
         if S == "1":
             contact_restorer()
         elif S == "2":
             delete_from_recyclebin()
         elif S == "3":
             return
         else:
             print("Invalid Input! Please try Again")
             return
    except FileNotFoundError:
        print("Recycle Bin file not found.")   
def contact_restorer():#-------------------------------------------------------------------------------------------CONTACT RESTORE
    contacts_file = "Contacts.csv"
    recycle_file = "recycle_bin.csv"
    restored = False
    rows = []
    name_or_number = input("Enter the Name or Number that you want to restore: ")
    try:
        with open(recycle_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].lower() == name_or_number.lower() or row[1] == name_or_number:
                    with open(contacts_file, "a", newline="") as cf:
                        writer = csv.writer(cf)
                        writer.writerow([row[0], row[1]])
                    restored = True
                else:
                    rows.append(row)
        with open(recycle_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        if restored:
            print(f"Contact '{name_or_number}' restored successfully.")
            q=input("Do you want to restore another contact?(yes/no): ")
            if(q.lower()!='yes'):
               return
        else:
            print(f"Contact '{name_or_number}' not found in recycle bin.")
            return
    except FileNotFoundError:
        print("Recycle bin file not found.")
        return
def delete_from_recyclebin():#----------------------------------------------------------------------------------RECYCLE BIN DELETE
    recycle_file = "recycle_bin.csv"
    name_or_number = input("Enter Name or Number to permanently delete: ").strip()
    rows = []
    deleted = False
    with open(recycle_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].lower() == name_or_number.lower() or row[1] == name_or_number:
                confirm = input(f" Are you sure you want to permanently delete '{row[0]} ({row[1]})'? (yes/no): ").strip().lower()
                if confirm == "yes":
                    deleted = True
                    continue
                elif confirm == 'no':
                   rows.append(row)
                else:
                   print("Invalid Input!")
                   return
            else:
                rows.append(row)
    with open(recycle_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    if deleted:
        print(f"Contact '{name_or_number}' permanently deleted from recycle bin.")
        w=input("Do you want to delete another contact?(yes/no): ")
        if(w.lower()!='yes'):
           return
    else:
        print(f"Deletion cancelled or Contact '{name_or_number}' not found in recycle bin.")
    return  
def menu():#------------------------------------------------------------------------------------------------------------------MENU          
  recycle_bin_emptier()
  while True:
    print('\n^0^-.-Contact Stop-.-^0^')
    print('1. View Contacts')
    print('2. Add Contacts')
    print('3. Search Contact')
    print('4. Delete Contacts') #recycle bin
    print('5. Exit')
    try:
      A=int(input("Enter the task number to start the task: "))
    except ValueError:
      print("Invalid Input! Please try Again(1-5)")
      continue
    if A==1:
      contact_viewer()
    elif A==2:
      contact_adder()
    elif A==3:
      Contact_searcher()
    elif A==4:
      Contact_deleter()  #working on recycle bin
    elif A==5:
      print('Exiting the program...')
      print('Thank you for using the program!')
      exit()
    else:
      print('Invalid Input! please try again..')
menu()