import datetime as dt
import PySimpleGUI as sg
persons_arr = [] #Array of arrays with all data from CSV import
persons_dict = [] #Array of dictionarys with all date from everyone having been born this day
current_date = dt.date.today().strftime("%d.%m.%Y") #current date
current_hour = dt.datetime.now().hour #current hour
error_message = ""

def Error_ourput(error):#array of all errors
    Error_layout_arr = []
    error_message = error
    Error_layout_arr.append([sg.Text("Error: " + str(error_message) + "please change")])
    Error_layout_arr.append([sg.Button("Schließen")])
    window = sg.Window('Window Title', Error_layout_arr)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Schließen': # if user closes window or clicks cancel
            break

def main_funktion():#contains all necessary methods and functions
    with open("input.csv", "r") as file:
        for line in file:
            persons_arr.append(line.strip().split(","))#adds per
        
    for i in range(len(persons_arr)):    
        try:
            dt.datetime.strptime(persons_arr[i][2], "%d.%m.%Y")
        except:
            ValueError
            error_message = "Date format should be DD.MM.YYYY"
            Error_ourput(error_message)
            raise ValueError("Date format should be DD.MM.YYYY")
            
        

    def compare_date(date_1,date_2)->bool:        
        compare_1 = dt.datetime.strptime(date_1, "%d.%m.%Y").strftime("%d.%m")#strips dates to compare day and month
        compare_2 = dt.datetime.strptime(date_2, "%d.%m.%Y").strftime("%d.%m")
        if  compare_1 == compare_2:
            return True
        else:
            return False
        
    def get_age(person_to_be_determined):
        age_to_be_determined = dt.datetime.strptime(person_to_be_determined["bd"],"%Y")
        #time_delta = int(dt.datetime.strptime(current_date,"%Y")) - int(age_to_be_determined)
        #return time_delta

    for person in persons_arr:
        if(len(person) < 4):
            error_message = "Csv incomplete, Csv Format should be: surname,firstname,date of birth(dd.mm.yyyy),gender(,image)"
            Error_ourput(error_message)
            raise ValueError("Csv incomplete, Csv Format should be: surname,firstname,date of birth(dd.mm.yyyy),gender(,image)")
        
        if(len(person) == 4 and compare_date(str(current_date),str(person[2]))):
            persons_dict.append({ #persons dict for persons without picture
            "firstname": person[1],
            "lastname": person[0],
            "bd": person[2],
            "gender": person[3],
            }) 
        elif(len(person) == 5 and compare_date(str(current_date),str(person[2]))): 
            persons_dict.append({ #persons dict for persons with picture
                "firstname": person[1],
                "lastname": person[0],
                "bd": person[2],
                "gender": person[3],
                "image": person[4],
            })  
            if not(person[4].endswith(".png")):#checks if files are end on .png
                error_message = "Images must be .png"
                Error_ourput(error_message)
                raise ValueError("Images must be .png")
        if(len(person) == 6):#checks if list length if correct(>=5)
            error_message = "Csv can't have more than 6 components"
            Error_ourput(error_message)
            raise ValueError("Csv can't have more than 6 components")
    
    for birthday_person in persons_dict:
        print(get_age(birthday_person))

    sg.theme('DarkBlue8')
    layout_arr = [] #layout of the birthday display
    layout_arr.append([sg.Text('Geburtstagskalender')])#checks if there are birthdays
    if len(persons_dict) == 0:
        layout_arr.append([sg.Text("Heute hat niemand Geburtstag")])
    for i in range(len(persons_dict)):
        layout_arr.append([sg.Text(f"heute hat {persons_dict[i]['firstname']} {persons_dict[i]['lastname']} ({persons_dict[i]['gender']}) geburtstag \n")])#prints the birthday message
        if "image" in persons_dict[i].keys():
            layout_arr.append([sg.Image(persons_dict[i]["image"])])
    layout_arr.append([sg.Button("Schließen")])
    # Create the Window
    window = sg.Window('Window Title', layout_arr)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Schließen': # if user closes window or clicks cancel
            break
        elif current_hour == 0:#reopens the window at the beginning of the day to display new birthdays
            window.close()
            main_funktion()
    
    window.close()
main_funktion()

