import pygame
import time
import random
from copy import copy, deepcopy
from turtle import *
from tkinter import *
import math

black = (0,0,0)
white = (255,255,255)
blue =  (0,0,255)
green = (0,255,0)
red =   (255,0,0)
yellow =(255,255,0)
cyan = (0,255,255)
magenta = (255,0,255)
silver = (192,192,192)
grey = (128,128,128)
maroon = (128,0,0)
olive = (128,128,0)
green2 = (0,128,0)
purple = (128,0,128)
teal = (0,128,128)
navy = (0,0,128)
salmon = (250,128,114)
pink = (255,105,180)
brown = (139,69,19)

pygame.init()
output_ = pygame.display.set_mode((1440, 720))
pygame.display.set_caption("4D modelling Output")

output_.fill(white)

input_ui_state_list = ["create user", "login", "view existing objects", "create new object"]
input_ui_state = input_ui_state_list[1]

def fsm_ui(ui_change):
    global input_ui_state_list
    global input_ui_state
    #input_ui_state_list and input_ui_state define the possible states and current state of the finite state machine respectivly

    def hashpassword(password, username):
        password = str(password)
        password += str(username)
        #the hash adds the username as a salt
        for i in range(0,23+len(password)):
            while len(password) < 4:
                password += str(ord(password[0]))
            hashed = 0
            for j in password:
                hashed = (hashed + (hashed << 19) + (hashed >> 13) + ord(j)) & 0xFFFFFFFF
            for j in str(hashed):
                hashed += hashed*int(j) & 0xF*(len(password)+5)
            hashedlen = len(str(hashed))
            while str(hashed)[-1] == "0" or len(str(hashed)) < hashedlen:
                hashed += int(str(hashed)[2:len(password)]) + (int(str(hashed)[2:len(password)]))%17
            password = str(hex(hashed))[2:]
        return password
        #the hashing algorithm produces a 8 hex character hash
        #over 4 thousand million possible hashing outcomes

    def create_user_gui():
        def change_fsm_1():
            createuser.destroy()
            fsm_ui(1)
            #this exits create new user back to login
        def create_user():
            username = str(username_input.get())
            password = str(password_input.get())
            password2 = str(repassword_input.get())
            useable_characters = str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_,.#!£$&")#all allowed characters
            if password != password2:
                error_label["text"] = "the passwords are not the same"
                return
            #checks if the passwords are the same
            usernamepassword = username + password
            for i in usernamepassword:
                acceptablecharacter = False
                for j in useable_characters:
                    if i == j:
                        acceptablecharacter = True
                if acceptablecharacter == False:
                    error_label["text"] = "One or more charaters you have entered are not allowed"
                    return
            #checks if all charaters are allowed
            f = open("users.txt", "r")
            g = f.read()
            userlist = g.split("  ")
            count = 0
            for i in userlist:
                userlist[count] = userlist[count].split(" ")
                count += 1
            f.close()
            for i in userlist:
                if i[0] == username:
                    error_label["text"] = "the username is already taken"
                    return
            #checks to see if the username is already taken
            f = open("users.txt", "a")
            f.write(username)
            f.write(" ")
            hashedpassword = hashpassword(password, username)
            f.write(hashedpassword)
            f.write("  ")
            f.close()
            userObjecttest = open("user objects.txt", "r")
            userObjecttestp2 = userObjecttest.read()
            userObjecttest.close()
            f = open("user objects.txt", "a")
            if userObjecttestp2 != "":
                f.write("  ")
            f.write(username)
            f.close()
            error_label["text"] = "new user created"
            return
            #if all checks above have been passed, then the new user will be created

        createuser = Tk()
        createuser.configure()
        createuser.geometry("360x174")
        createuser.resizable(0, 0)
        createuser.title("Create New User")

        create_user_frame = Frame(createuser, width=360, height=108)
        create_user_frame.pack()

        username_label = Label(create_user_frame, text = "  enter username: ").grid(row = 0, column = 0, padx = 1, pady = 1)
        username_input = Entry(create_user_frame, bd = 1)
        username_input.grid(row = 0, column = 1, padx = 1, pady = 1)
        password_label = Label(create_user_frame, text = "  enter password: ").grid(row = 1, column = 0, padx = 1, pady = 1)
        password_input = Entry(create_user_frame, show="*", bd = 1)
        password_input.grid(row = 1, column = 1, padx = 1, pady = 1)
        repassword_label = Label(create_user_frame, text = "reenter password: ").grid(row = 2, column = 0, padx = 1, pady = 1)
        repassword_input = Entry(create_user_frame, show="*", bd = 1)
        repassword_input.grid(row = 2, column = 1, padx = 1, pady = 1)

        createuserbutton = Button(create_user_frame, text = "create user", command = lambda : create_user(), bd = 1).grid(row = 3, column = 1, padx = 1, pady = 1)
        empty_label = Label(create_user_frame, text = "").grid(row = 4, column = 1, padx = 1, pady = 1)
        back_button = Button(create_user_frame, text = "back to login", command = lambda : change_fsm_1(), bd = 1).grid(row = 5, column = 1, padx = 1, pady = 1)
        error_label = Label(createuser, text = "")
        error_label.pack()

    def login():
        def change_fsm_2(change):
            user.destroy()
            fsm_ui(change)
            #this exits login and either goes to create_new_user or to view_4d_object
        def checkusernamepassword():
            f = open("users.txt", "r")
            usernamepasswordlist = f.read()
            f.close()
            usernamepasswordlist = usernamepasswordlist[:-2]
            usernamepasswordlist = usernamepasswordlist.split("  ")
            count = 0
            for i in usernamepasswordlist:
                usernamepasswordlist[count] = usernamepasswordlist[count].split(" ")
                count += 1
            usernameexists = False
            for i in usernamepasswordlist:
                if i[0] == user_entry_username.get():
                    usernameexists = True
                    indexno = usernamepasswordlist.index(i)
            if usernameexists == True:
                if usernamepasswordlist[indexno][1] == hashpassword(user_entry_password.get(), user_entry_username.get()):
                    f = open("current user.txt", "w")
                    f.write(user_entry_username.get())
                    f.close()
                    change_fsm_2(1)
                else:
                    user_label_whitespace["text"] = "The password was incorrect"
            else:
                user_label_whitespace["text"] = "The username could not be found"
            #the login checks to see if the user exists before checking to see if the password is correct
            #it outputs the appropriate response

        user = Tk()
        user.configure()
        user.geometry("360x144")
        user.resizable(0, 0)
        user.title("Enter User")

        output_.fill(black)
        pygame.display.flip()

        topFrame = Frame(user, width = 360, height = 24)
        white_label = Label(topFrame, text = "       ").grid(row = 0, column = 0, padx = 1, pady = 1)
        user_label = Label(topFrame, text = "                      enter username and password:                     ").grid(row = 0, column = 1, padx = 1, pady = 1)
        quitButton = Button(topFrame, text = "Quit", command = lambda : quit(), bd = 1)
        quitButton.grid(row = 0, column = 2, padx = 1, pady = 1)
        user_entry_username = Entry(user, bd = 1)
        user_entry_password = Entry(user, show="*", bd = 1)
        user_button = Button(user, text = "   Next   ", command = lambda : checkusernamepassword(), bd = 1)
        user_label_whitespace = Label(user, text = "")
        user_createuserbutton = Button(user, text = "  or create a new user", command = lambda : change_fsm_2(-1), bd = 1)

        topFrame.pack()
        user_entry_username.pack()
        user_entry_password.pack()
        user_button.pack()
        user_label_whitespace.pack()
        user_createuserbutton.pack()

    def view_4d_object():
        def change_fsm_3(change):
            view_object.destroy()
            fsm_ui(change)
            #this exits view_4d_objects and either goes to login or create_new_4d_object
        def draw():
            if objects[-1] != "current object":
                objects.append("current object")
            output_.fill(white)
            pygame.display.flip()
            file = str(dropdown.get()) + ".txt"
            f = open(file, "r")
            h = f.read()
            if file == "current object.txt" and h == "":
                empty_label_1["text"] = "ERROR: current object allows you to continue to adjust your last output."
                empty_label_1a["text"] = "It cannot be used before rendering annother object."
                return
            else:
                empty_label_1["text"], empty_label_1a["text"] = "", ""
            h = h.split("   ")
            count = 0
            for i in h:
                count2 = 0
                h[count] = h[count].split("  ")
                for j in h[count]:
                    count3 = 0
                    h[count][count2] = h[count][count2].split(" ")
                    for k in h[count][count2]:
                        h[count][count2][count3] = float(h[count][count2][count3])
                        count3 += 1
                    count2 += 1
                count += 1
            f.close()
            #the above for loops extrapolates the data from the appropriate text file and puts it into a 3D array named h

            rotno = 1   #number of rotations
            sliderlist=[xy_slider.get(), xz_slider.get(), xw_slider.get(), yz_slider.get(), yw_slider.get(), zw_slider.get()]
            count = -1
            if tickbox.get() == True:
                for i in range(0, len(sliderlist)):
                    count += 1
                    try:
                        if 1+(360/abs(sliderlist[count]))-1%((360/abs(sliderlist[count]))) > rotno:
                            rotno = 1+(360/abs(sliderlist[count]))-1%((360/abs(sliderlist[count])))
                    except:
                        pass
                if rotno > 100:
                    rotno = 100
                elif rotno < 20:
                    rotno = 20
                    #sets a cap to the number of rotations on 100 and a min to 20

            enlargevar = enlargeentry.get()
            if enlargevar == "":
                enlargevar = 1
            count = 0
            try:
                enlargevar = float(enlargevar)
            except:
                empty_label_1["text"] = "ERROR: enlargement does not contain a real number."
                return
            for i in h[0]:
                h[0][count] = matrix(0, h[0][count], float(enlargevar))
                count+=1
            #enlarges the object

            for i in range(0, int(rotno)):
                count=0
                for i in h[0]:
                    count2 = 1
                    for j in sliderlist:
                        if j != 0:
                            h[0][count] = matrix(count2, h[0][count], j)
                        count2 += 1
                    count += 1
                    #rotates the object using the matrix function I created

                count = 0
                largestvalue = 0
                for i in h[0]:
                    currentmod = float(math.sqrt(((h[0][count][0])**2)+((h[0][count][1])**2)+((h[0][count][2])**2)+((h[0][count][3])**2)))
                    if currentmod > largestvalue:
                        largestvalue = currentmod
                    count+=1
                largestvalue += largestvalue + 2 - 1%largestvalue
                #this deceides the 'point of view' for a perpective projection.
                #this ensures that the point of view has a larger modulus than any coordinate in the object
                #if this is not the case, It would result in a divide by zero error or incorrect mapping

                hdraw = deepcopy(h[0])
                #hdraw is used to project h down to 2D without altering h so that h could be used for multiple rotations

                count = 0
                for i in hdraw:
                    hdraw[count] = matrix(objects2.index(dropdown2.get())+7, hdraw[count], largestvalue)
                    count += 1
                    #this uses the matricies to project the coordinates down to 2D

                output_.fill(white) #refreshes output

                count = 0
                for i in h[1]:
                    count = 1
                    for j in range(0, len(i)-1):
                        pygame.draw.line(output_, red, [(hdraw[int(i[0])][0])+720, -(hdraw[int(i[0])][1])+360], [(hdraw[int(i[count])][0])+720, -(hdraw[int(i[count])][1])+360], 3)
                        pygame.display.flip()
                        count+=1
                        #draws lines between appropraite verticies
                time.sleep(0.025)

            g = open("current object.txt", "w")
            gstring = ""
            for i in h:
                for j in i:
                    for k in j:
                        gstring += str(k)+" "
                    gstring += " "
                gstring += " "
            g.write(gstring[:-3])
            g.close()
            return
            #this stores the last object in a file so that they could continue viewing it without it resetting

        view_object = Tk()
        view_object.geometry("624x540")
        view_object.title("View existing 4D object")
        view_object.resizable(0, 0)

        output_.fill(white)
        pygame.display.flip()

        tickbox = BooleanVar()
        tickbox2 = BooleanVar()
        dropdown = StringVar(view_object)
        dropdown2 = StringVar(view_object)

        objects = ["5cell", "tesseract", "16cell"]
        f = open("user objects.txt", "r")
        g = open("current user.txt", "r")
        currentUser = g.read()
        customObjects = f.read()
        customObjects = customObjects.split("  ")
        count=0
        for i in customObjects:
            customObjects[count] = customObjects[count].split(" ")
            count += 1
        count=0
        for i in customObjects:
            if i[0] == currentUser and len(customObjects[count]) != 1:
                count2=1
                for j in range(0,len(customObjects[count])-1):
                    objects.append(customObjects[count][count2])
                    count2+=1
            count+=1
        objects.append("current object")
        dropdown.set(objects[1])

        objects2 = ["orthogonal projection", "perspective projection"]#list of projections
        dropdown2.set(objects2[0])

        g = open("current object.txt", "w")
        g.close()

        label_0 = Label(view_object, text = "select object and projection:")
        objectselect = OptionMenu(view_object, dropdown, *objects)
        empty_label_1 = Label(view_object, text = "")
        empty_label_1a = Label(view_object, text = "")

        animated_rotation = Checkbutton(view_object, text="animated rotations", variable=tickbox)
        perspective = Checkbutton(view_object, text="perspective projection", variable=tickbox2)
        perspectiveselect = OptionMenu(view_object, dropdown2, *objects2)

        optionframe = Frame(view_object, width = 624, height = 24)

        backtologin = Button(optionframe, text = " Log Out ", command = lambda : change_fsm_3(-1), bd = 1)
        backtologin.grid(row = 0, column = 0, padx = 1, pady = 1)
        optionlabel = Label(optionframe, text = " "*150).grid(row = 0, column = 1, padx = 1, pady = 1)
        createobject = Button(optionframe, text = "Create new obejct", command = lambda : change_fsm_3(1), bd = 1)
        createobject.grid(row = 0, column = 2, padx = 1, pady = 1)

        sliderframe = Frame(view_object, width = 312, height = 64)

        enlarge_label = Label(sliderframe, text = "                   enlargement factor: ").grid(row = 0, column = 0, padx = 1, pady = 1)
        rot_label = Label(sliderframe, text = "rotation around    ").grid(row = 1, column = 0, padx = 1, pady = 1)
        xy_s_label = Label(sliderframe, text = "xy plane: ").grid(row = 2, column = 0, padx = 1, pady = 1)
        xz_s_label = Label(sliderframe, text = "xz plane: ").grid(row = 3, column = 0, padx = 1, pady = 1)
        xw_s_label = Label(sliderframe, text = "xw plane: ").grid(row = 4, column = 0, padx = 1, pady = 1)
        yz_s_label = Label(sliderframe, text = "yz plane: ").grid(row = 5, column = 0, padx = 1, pady = 1)
        yw_s_label = Label(sliderframe, text = "yw plane: ").grid(row = 6, column = 0, padx = 1, pady = 1)
        zw_s_label = Label(sliderframe, text = "zw plane: ").grid(row = 7, column = 0, padx = 1, pady = 1)
        xy_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        enlargeentry = Entry(sliderframe, bd = 1)
        enlargeentry.grid(row = 0, column = 1, padx = 1, pady = 1)
        slider_label = Label(sliderframe, text = "slider").grid(row = 1, column = 1, padx = 1, pady = 1)
        xy_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        xy_slider.grid(row = 2, column = 1, padx = 1, pady = 1)
        xz_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        xz_slider.grid(row = 3, column = 1, padx = 1, pady = 1)
        xw_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        xw_slider.grid(row = 4, column = 1, padx = 1, pady = 1)
        yz_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        yz_slider.grid(row = 5, column = 1, padx = 1, pady = 1)
        yw_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        yw_slider.grid(row = 6, column = 1, padx = 1, pady = 1)
        zw_slider = Scale(sliderframe, from_=-180, to=180, length=360, orient=HORIZONTAL)
        zw_slider.grid(row = 7, column = 1, padx = 1, pady = 1)
        white_space_label = Label(view_object, text = "")
        drawbutton = Button(view_object, text = "   Draw   ", command = lambda : draw(), bd = 1)

        optionframe.pack()
        label_0.pack()
        objectselect.pack()
        perspectiveselect.pack()
        animated_rotation.pack()
        empty_label_1.pack()
        empty_label_1a.pack()
        sliderframe.pack()
        white_space_label.pack()
        drawbutton.pack()

        view_object.mainloop()

    def create_new_4d_object():
        def change_fsm_4():
            input_.destroy()
            fsm_ui(-1)
        #this exits create_new_4d_object and goes to view_4d_object
        def confirm_back():
            if len(coordinate_list[1]) != 0:
                confirmationUI("Your unsaved object will be lost. Are you sure?", None, None, None)
            else:
                change_fsm_4()

        def confirmationUI(error, userObjectList, userIndex, name):
            def confirmationEnd(error, userObjectList, userIndex, name):
                if error == "Your unsaved object will be lost. Are you sure?":
                    confirm.destroy()
                    change_fsm_4()
                elif error == "Object already exists. Do you wish to replace it?":
                    d = open("user objects.txt", "w")
                    listStr = ""
                    for i in userObjectList:
                        for j in i:
                            listStr += str(j)+" "
                        listStr += " "
                    d.write(listStr[:-2])
                    d.close()
                    fileName = name + ".txt"
                    h = open(fileName, "w")
                    objectStr = ""
                    for i in coordinate_list:
                        for j in i:
                            for k in j:
                                objectStr += str(k)+" "
                            objectStr += " "
                        objectStr += " "
                    h.write(objectStr[:-3])
                    h.close()
                    confirm.destroy()
                else:
                    print("an error has occurred")

            #the UI below is used for confirmations
            confirm = Tk()
            confirm.geometry("270x80")
            confirm.title("")
            confirm.resizable(0, 0)

            whitespaceLabel = Label(confirm, text="")
            question = Label(confirm, text=(str(error)))
            buttonFrame = Frame(confirm, width = 312, height = 24)
            if error != "You have reached the recommended vertex limit":
                yes = Button(buttonFrame, text = "  Yes  ", command = lambda : confirmationEnd(error, userObjectList, userIndex, name), bd = 1)
                yes.grid(row = 0, column = 0, padx = 1, pady = 1)
                no = Button(buttonFrame, text = "  No  ", command = lambda : confirm.destroy(), bd = 1)
                no.grid(row = 0, column = 1, padx = 1, pady = 1)
            elif error == "You have reached the recommended vertex limit":
                ok = Button(buttonFrame, text = "  Ok  ", command = lambda : confirm.destroy(), bd = 1)
                ok.grid(row = 0, column = 0, padx = 1, pady = 1)
            else:
                print("an error has occurred")
                #these else statements should not run, they are only programmed for defensive programming only
            whitespaceLabel.pack()
            question.pack()
            buttonFrame.pack()

        def errorClear():
            #this function clears the whitespace labels of errors and other messages
            error_label["text"] = ""
            error_label2["text"] = ""
            try:
                errorLabelSave["text"] = ""
            except:
                pass
            return

        def add_vertex():
            #this function adds a vertex to the object the user is creating
            errorClear()
            x = x_point_input.get()
            y = y_point_input.get()
            z = z_point_input.get()
            w = w_point_input.get()

            #this try except statement checks to see if the user has only entered numbers
            try:
                x = float(x)
                y = float(y)
                z = float(z)
                w = float(w)
            except:
                error_label["text"] = "Please enter suitable numbers"
                return

            for i in coordinate_list[0]:
                if i[0] == x and i[1] == y and i[2] == z and i[3] == w:
                    error_label["text"] = "vertex already exists"
                    return

            #the following 2 lines add hte vertex to the 3D array
            coordinate_list[0].append([x, y, z, w, len(coordinate_list[0])])
            coordinate_list[1].append([len(coordinate_list[0])-1])

            #these are all the colours that are used when outputting the object in the pygame window
            colours = [blue, green, yellow, cyan, magenta, silver, grey, maroon, olive, green2, purple, teal, navy, salmon, pink, brown]

            #the labels below are used to show the used what the entered
            #the information the used has extered is appended to the 'table of labels'
            label = Label(listFrame, text = x).grid(row = len(coordinate_list[0]), column = 0, padx = 1, pady = 1)
            label2 = Label(listFrame, text = y).grid(row = len(coordinate_list[0]), column = 1, padx = 1, pady = 1)
            label3 = Label(listFrame, text = z).grid(row = len(coordinate_list[0]), column = 2, padx = 1, pady = 1)
            label4 = Label(listFrame, text = w).grid(row = len(coordinate_list[0]), column = 3, padx = 1, pady = 1)
            label5 = Label(listFrame, text = len(coordinate_list[0])-1).grid(row = len(coordinate_list[0]), column = 4, padx = 1, pady = 1)
            coords = [x, y, z, w]
            count = 0
            for i in coords:
                if i%1 != 0:
                    #changes the cooridinates into the nearest integers
                    if i%1 < 0.5:
                        coords[count] -= i%1
                    else:
                        coords[count] += (1-(i%1))
                coords[count] = int(coords[count])
                count+=1
            #adds the coordinates to the pygame output
            pygame.draw.circle(output_, colours[len(coordinate_list[1])%len(colours)], ((coords[0]*2)+360,360-(coords[1]*2)), 4, 4)
            pygame.draw.circle(output_, colours[len(coordinate_list[1])%len(colours)], ((coords[3]*2)+1080,360-(coords[2]*2)), 4, 4)
            pygame.display.flip()

            if len(coordinate_list[1]) == 16:
                confirmationUI("You have reached the recommended vertex limit", None, None, None)
            #the reason why this message appears is because after 16 verticies has been entered is because:
                #the pygmae output would have run out of unique colours and colours whould be reused
                #the 'table of labels' would have reached the default size of the 'create new 4D object' UI
                    #as a result, that UI exclusivly can be changed in size

        def add_edge():
            #this function adds an edge to the object the user is creating
            errorClear()
            #this try except statement checks to see it the user has entered an integer
            try:
                vertexA = int(joinA.get())
                vertexB = int(joinB.get())
            except:
                error_label2["text"] = "Please ensure your have entered an integer"
                return

            #this if, elif statement checks if the verticies are different and exists
            if vertexA == vertexB:
                error_label2["text"] = "Please enter different vertex numbers"
                return
            elif vertexA < 0 or vertexA > len(coordinate_list[0])-1 or vertexB < 0 or vertexB > len(coordinate_list[0])-1:
                error_label2["text"] = "Please ensure that the vertecies entered exists"
                return

            #the if statement switches vertexA and vertexB if vertexA is larger than vertexB, so that vertexB is always larger than vertexA
            if vertexA > vertexB:
                vertexC = vertexA
                vertexA = vertexB
                vertexB = vertexC

            #this for loop checks to see if the edge already exists
            for i in coordinate_list[1][vertexA][1:]:
                if vertexB == i:
                    error_label2["text"] = "Edge already exists"
                    return

            coordinate_list[1][vertexA].append(vertexB)
            label = Label(listFrame, text = coordinate_list[1][vertexA][1:]).grid(row = coordinate_list[1][vertexA][0]+1, column = 5, padx = 1, pady = 1)
            pygame.draw.line(output_, red, [(coordinate_list[0][vertexA][0]*2)+360, 360-(coordinate_list[0][vertexA][1]*2)], [(coordinate_list[0][vertexB][0]*2)+360, 360-(coordinate_list[0][vertexB][1]*2)], 1)
            pygame.draw.line(output_, red, [(coordinate_list[0][vertexA][3]*2)+1080, 360-(coordinate_list[0][vertexA][2]*2)], [(coordinate_list[0][vertexB][3]*2)+1080, 360-(coordinate_list[0][vertexB][2]*2)], 1)
            pygame.display.flip()
            #the code above draws a red edge between the vertices that had been entered
            return

        def create(coordinate_list):
            #the create function create a new text file for the object and saves the object in that file
            def closeSave():
                #this closes the save UI
                save.destroy()
                return
            def save4dObject(name):
                name=str(name)
                f = open("user objects.txt", "r")
                g = open("current user.txt", "r")
                currentUser = g.read()
                g.close()
                userObjectList = f.read()
                f.close()
                userObjectList = userObjectList.split("  ")
                count=0
                userIndex=0
                for i in userObjectList:
                    userObjectList[count] = userObjectList[count].split(" ")
                    if userObjectList[count][0] == currentUser:
                        userIndex = count
                    count+=1
                for i in userObjectList:
                    for j in i:
                        if j == name:
                            if i.index(j) != 0 and i[0] == currentUser:
                                #checks if the object already exists and asking if the user wants to replace it
                                #this is only an option if the object already exists under the user that is currently logged in
                                confirmationUI("Object already exists. Do you wish to replace it?", userObjectList, userIndex, name)
                            else:
                                errorLabelSave["text"] = "Name already in use, please use another"
                            return
                #the code below saves the object that the user has created under a new text file in the variabe 'name'
                userObjectList[userIndex].append(name)
                d = open("user objects.txt", "w")
                listStr = ""
                for i in userObjectList:
                    for j in i:
                        listStr += str(j)+" "
                    listStr += " "
                d.write(listStr[:-2])
                d.close()
                fileName = name + ".txt"
                h = open(fileName, "w")
                objectStr = ""
                #the for loops below change the 3D array into a string for it to be stored in the text file
                for i in coordinate_list:
                    for j in i:
                        for k in j:
                            objectStr += str(k)+" "
                        objectStr += " "
                    objectStr += " "
                h.write(objectStr[:-3])
                h.close()
                errorLabelSave["text"] = str(name) + " succsessfully created under " + str(userObjectList[userIndex][0])
                return

            errorClear()

            #below is the save UI
            save = Tk()
            save.geometry("240x98")
            save.title("Save")
            save.resizable(0, 0)

            closeFrame = Frame(save, width = 312, height = 24)
            nameframe = Frame(save, width = 312, height = 24)

            leftLabel = Label(closeFrame, text=" "*63).grid(row=0, column=0, padx=1, pady=1)
            closeButton = Button(closeFrame, text = " Close ", command = lambda : closeSave(), bd = 1)
            closeButton.grid(row = 0, column = 1, padx = 1, pady = 1)
            name_label = Label(nameframe, text = "enter name: ").grid(row = 0, column = 0, padx = 1, pady = 1)
            name_entry = Entry(nameframe, bd = 1)
            name_entry.grid(row = 0, column = 1, padx = 1, pady = 1)
            fileLabel = Label(nameframe, text=".txt").grid(row = 0, column = 2, padx = 1, pady = 1)
            saveobject = Button(save, text = " Save ", command = lambda : save4dObject(name_entry.get()), bd = 1)
            errorLabelSave = Label(save, text = "")

            closeFrame.pack()
            nameframe.pack()
            saveobject.pack()
            errorLabelSave.pack()

        #below is the code that splits the pygame module in 2.
        #The left half is used to the x-y plane and the right half is used for the z-w plane
        output_.fill(white)
        pygame.draw.line(output_, black, [720, 0], [720, 720], 1)
        #the lines below draws axis and labels in the bottom left corner of each half of the pygame window
        pygame.draw.lines(output_, black, False, [[10,690],[10,710],[30,710]], 1)
        pygame.draw.lines(output_, black, False, [[5,695],[10,690],[15,695]], 1)
        pygame.draw.lines(output_, black, False, [[25,705],[30,710],[25,715]], 1)
        pygame.draw.lines(output_, black, False, [[730,690],[730,710],[750,710]], 1)
        pygame.draw.lines(output_, black, False, [[725,695],[730,690],[735,695]], 1)
        pygame.draw.lines(output_, black, False, [[745,705],[750,710],[745,715]], 1)
        pygame.draw.line(output_, black, [5, 685], [15, 675], 1)
        pygame.draw.line(output_, black, [5, 675], [15, 685], 1)
        pygame.draw.line(output_, black, [40, 710], [36, 705], 1)
        pygame.draw.line(output_, black, [36, 715], [44, 705], 1)
        pygame.draw.lines(output_, black, False, [[735,684],[725,684],[735,674],[725,674]], 1)
        pygame.draw.lines(output_, black, False, [[754,705],[759,715],[762,710],[765,715],[770,705]], 1)
        pygame.display.flip()

        #below is the 'create new 4D object UI'
        input_ = Tk()
        input_.geometry("624x660")
        input_.title("Create new 4D object")
        topframe = Frame(input_, width = 624, height = 64)
        topframe.pack()

        coordinate_list = [[], []]
        labelcount = 0

        backtoview = Button(topframe, text = "   Back   ", command = lambda : confirm_back(), bd = 1)
        backtoview.grid(row = 0, column = 0, padx = 1, pady = 1)
        rightlabel = Label(topframe, text = " "*185).grid(row = 0, column = 1, padx = 1, pady = 1)

        whitespace = Label(input_, text = "")
        whitespace2 = Label(input_, text = "")
        createobeject = Button(input_, text = " Save Object ", command = lambda : create(coordinate_list), bd = 1)
        input_frame = Frame(input_, width = 312, height = 64)

        x_label = Label(input_frame, text = "x coordinate").grid(row = 0, column = 0, padx = 1, pady = 1)
        y_label = Label(input_frame, text = "y coordinate").grid(row = 0, column = 1, padx = 1, pady = 1)
        z_label = Label(input_frame, text = "z coordinate").grid(row = 0, column = 2, padx = 1, pady = 1)
        w_label = Label(input_frame, text = "w coordinate").grid(row = 0, column = 3, padx = 1, pady = 1)
        x_point_input = Entry(input_frame, bd = 1)
        x_point_input.grid(row = 1, column = 0, padx = 1, pady = 1)
        y_point_input = Entry(input_frame, bd = 1)
        y_point_input.grid(row = 1, column = 1, padx = 1, pady = 1)
        z_point_input = Entry(input_frame, bd = 1)
        z_point_input.grid(row = 1, column = 2, padx = 1, pady = 1)
        w_point_input = Entry(input_frame, bd = 1)
        w_point_input.grid(row = 1, column = 3, padx = 1, pady = 1)

        createvertex = Button(input_, text = "Add vertex", command = lambda : add_vertex(), bd = 1)
        error_label = Label(input_, text= "")

        moreinput_frame = Frame(input_, width = 312, height = 64)
        labelEdge = Label(moreinput_frame, text = "Join vertices with an edge: ").grid(row = 0, column = 0, padx = 1, pady = 1)
        joinA = Entry(moreinput_frame, bd = 1)
        joinA.grid(row = 0, column = 1, padx = 1, pady = 1)
        joinB = Entry(moreinput_frame, bd = 1)
        joinB.grid(row = 0, column = 2, padx = 1, pady = 1)
        createedge = Button(input_, text = "Add edge", command = lambda : add_edge(), bd = 1)
        error_label2 = Label(input_, text= "")

        createobeject.pack()
        whitespace.pack()
        input_frame.pack()
        createvertex.pack()
        error_label.pack()
        moreinput_frame.pack()
        createedge.pack()
        error_label2.pack()
        whitespace2.pack()

        #below is the frame used for the 'table of labels'
        listFrame = Frame(input_, width = 624, height = 1)

        frameLabel1 = Label(listFrame, text = " x coordinate: ").grid(row = 0, column = 0, padx = 1, pady = 1)
        frameLabel2 = Label(listFrame, text = "|   y coordinate: ").grid(row = 0, column = 1, padx = 1, pady = 1)
        frameLabel3 = Label(listFrame, text = "|   z coordinate: ").grid(row = 0, column = 2, padx = 1, pady = 1)
        frameLabel4 = Label(listFrame, text = "|   w coordinate: ").grid(row = 0, column = 3, padx = 1, pady = 1)
        frameLabel5 = Label(listFrame, text = "|   vertex no.: ").grid(row = 0, column = 4, padx = 1, pady = 1)
        frameLabel6 = Label(listFrame, text = "|   connected vertices: ").grid(row = 0, column = 5, padx = 1, pady = 1)

        listFrame.pack()


    #the line below changes the state of the finite state machine
    input_ui_state = input_ui_state_list[input_ui_state_list.index(input_ui_state) + ui_change]
    #the if and elif statements below run the UI required for the current state of the FSM
    if input_ui_state == input_ui_state_list[0]:
        create_user_gui()
    elif input_ui_state == input_ui_state_list[1]:
        login()
    elif input_ui_state == input_ui_state_list[2]:
        view_4d_object()
    elif input_ui_state == input_ui_state_list[3]:
        create_new_4d_object()
    else:
        print("an error has occurred")


def matrix(matrix_type, coordinates, variable):
    #the matrix_type is an integer from 0-9 and determines the matrix that is used
    #coordinates has to be a list of 4 coordinates
    #variable would either be an multiplier, angle or perspective factor
    def enlargement(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = coordinates[0]*variable
        new_coordinates[1] = coordinates[1]*variable
        new_coordinates[2] = coordinates[2]*variable
        new_coordinates[3] = coordinates[3]*variable
        return new_coordinates

    def xyrotation(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = 0 + coordinates[0]*math.cos(variable) + coordinates[1]*math.sin(variable)
        new_coordinates[1] = 0 - coordinates[0]*math.sin(variable) + coordinates[1]*math.cos(variable)
        new_coordinates[2] = 0 + coordinates[2]
        new_coordinates[3] = 0 + coordinates[3]
        return new_coordinates

    def xzrotation(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = 0 + coordinates[0]*math.cos(variable) - coordinates[2]*math.sin(variable)
        new_coordinates[1] = 0 + coordinates[1]
        new_coordinates[2] = 0 + coordinates[0]*math.sin(variable) + coordinates[2]*math.cos(variable)
        new_coordinates[3] = 0 + coordinates[3]
        return new_coordinates

    def xwrotation(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = 0 + coordinates[0]*math.cos(variable) + coordinates[3]*math.sin(variable)
        new_coordinates[1] = 0 + coordinates[1]
        new_coordinates[2] = 0 + coordinates[2]
        new_coordinates[3] = 0 - coordinates[0]*math.sin(variable) + coordinates[3]*math.cos(variable)
        return new_coordinates

    def yzrotation(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = 0 + coordinates[0]
        new_coordinates[1] = 0 + coordinates[1]*math.cos(variable) + coordinates[2]*math.sin(variable)
        new_coordinates[2] = 0 - coordinates[1]*math.sin(variable) + coordinates[2]*math.cos(variable)
        new_coordinates[3] = 0 + coordinates[3]
        return new_coordinates

    def ywrotation(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = 0 + coordinates[0]
        new_coordinates[1] = 0 + coordinates[1]*math.cos(variable) - coordinates[3]*math.sin(variable)
        new_coordinates[2] = 0 + coordinates[2]
        new_coordinates[3] = 0 + coordinates[1]*math.sin(variable) + coordinates[3]*math.cos(variable)
        return new_coordinates

    def zwrotation(variable, coordinates):
        new_coordinates = [None]*4
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = 0 + coordinates[0]
        new_coordinates[1] = 0 + coordinates[1]
        new_coordinates[2] = 0 + coordinates[2]*math.cos(variable) + coordinates[3]*math.sin(variable)
        new_coordinates[3] = 0 - coordinates[2]*math.sin(variable) + coordinates[3]*math.cos(variable)
        return new_coordinates

    def orthogonal4dto3dto3d(coordinates):
        new_coordinates = [None]*2
        new_coordinates.append(coordinates[4])
        new_coordinates[0] = coordinates[0]
        new_coordinates[1] = coordinates[1]
        return new_coordinates

    def perspective4dto3dto2d(variable, coordinates):
        new_coordinates = [None]*3
        new2_coordinates = [None]*2
        new2_coordinates.append(coordinates[4])
        try:
            new_coordinates[0] = coordinates[0]*variable/(variable-coordinates[3])
            new_coordinates[1] = coordinates[1]*variable/(variable-coordinates[3])
            new_coordinates[2] = coordinates[2]*variable/(variable-coordinates[3])
            new_variable = (variable**2)/(variable-coordinates[3])
            new2_coordinates[0] = (new_coordinates[0]*new_variable)/(new_variable-new_coordinates[2])
            new2_coordinates[1] = (new_coordinates[1]*new_variable)/(new_variable-new_coordinates[2])
        except ZeroDivisionError:
            new_coordinates[0] = coordinates[0]*variable/(variable-coordinates[3]+0.01)
            new_coordinates[1] = coordinates[1]*variable/(variable-coordinates[3]+0.01)
            new_coordinates[2] = coordinates[2]*variable/(variable-coordinates[3]+0.01)
            new_variable = (variable**2)/(variable-coordinates[3]+0.01)
            new2_coordinates[0] = (new_coordinates[0]*new_variable)/(new_variable-new_coordinates[2]+0.01)
            new2_coordinates[1] = (new_coordinates[1]*new_variable)/(new_variable-new_coordinates[2]+0.01)
        return new2_coordinates

    #pythons math.trig functions work in radians, the if statement below changes the values which have been entered in degrees to radians
    if matrix_type > 0 and matrix_type < 7:
        variable = (variable/180)*math.pi
    variable = float(variable)
    #the if elif statements below run the matrix required. It depends on the variable matrix_type.
    if matrix_type == 0:
        return enlargement(variable, coordinates)
    elif matrix_type == 1:
        return xyrotation(variable, coordinates)
    elif matrix_type == 2:
        return xzrotation(variable, coordinates)
    elif matrix_type == 3:
        return xwrotation(variable, coordinates)
    elif matrix_type == 4:
        return yzrotation(variable, coordinates)
    elif matrix_type == 5:
        return ywrotation(variable, coordinates)
    elif matrix_type == 6:
        return zwrotation(variable, coordinates)
    elif matrix_type == 7:
        return orthogonal4dto3dto3d(coordinates)
    elif matrix_type == 8:
        return perspective4dto3dto2d(variable, coordinates)
    else:
        print("an error has occurred")

fsm_ui(0)#this calls upon and runs the FSM
