# Programmeringsteknik, webcourse at KTH.
# Adrian Lundhe
# P-assignment: no 176, Repeating word filter.

# The program takes in a text and processes all of the words. The idea is to 
# find repeating words and highlight them with a color. The default has been
# set to 40 words. It is possible, in the GUI, to add words that should not be 
# checked by adding them to the exception list.

# #############################################################################

from tkinter import *
from tkinter import filedialog
import os.path


# Fields of variables, constants and lists.

# File for words that are exceptions.
EXCEPTION_FILE = "exception_file.txt"
# Max words to filter per cycle.
NUMBER_OF_WORDS = 40
# Array of words that are exceptions.
exception_array = []


# Class Words - processing words from the text.
class Words:

    # Constructor.
    def __init__(self, content):
        self.content = content
        self.selected = 0
        self.sign = ""
        return


    # Seperates letters from other special signs. Later on the seperated words
    # will be checked from the list created with the seperated words, but all
    # types of characters will be saved for the final print to the user.
    def cleaner(self):
        # .isalnum(): Return true if all characters in the string are
        # alphanumeric and there is at least one character, false otherwise.
        if len(self.content) > 1:
            while not self.content[(len(self.content) - 1)].isalnum():
                self.sign = self.content[(len(self.content) - 1)] + self.sign
                self.content = self.content[:-1]
        else:
            if not self.content.isalnum():
                self.sign = self.content
                self.content = ""
        return


# Add content from a file to an array, row by row.
# Param: Name of the file with the text.
# Return: Array with the text.
def create_array(file_name):
    word_array = []
    if os.path.isfile(file_name):
        file = open(file_name, "r", encoding="utf-8")
        # Removes leading and ending whitespaces around words.
        word_array = [row.strip() for row in file]
        file.close()
    return word_array


# Checks if a string is in the array or not.
# Param: Words, Array with words
# Return: 1 if the word exists, else 0.
def word_in_array(word, array):
    result = 0
    if word.lower() in array:
        result = 1
        return result
    return result


# Saves the word in the array and optionally saves it to the exception file.
# Param: A word, If selected in GUI: save the word in file.
def save_exception(word, save_it):
    if save_it:
        file = open(EXCEPTION_FILE, "a", encoding="utf-8")
        file.write(word + "\n")
        file.close()
    exception_array.append(word)
    return


# Select the word-object if it is in the list with words.
# Check if the word exists: return it, else select it.
# Param: word = Word-object, word_array = list with strings.
# Return: the word.
def check_word(word, word_array):
    # Check and remove whitespace and seperation signs around the words.
    word.cleaner()
    # Get the word content and array and if word exists, return,
    # else if not in list...
    if word_in_array(word.content, word_array):
        if not word_in_array(word.content, exception_array):
            word.selected = 1
    return word


# Check repeating words from the text.
# Param: File with the text.
# Extra explanation: Removes whitespace between words.
# It may look like this: " I, said  ,that!!! ".
def check_text(file_name):
    word_array = NUMBER_OF_WORDS * [None]
    file = open(file_name, "r", encoding="utf-8")
    # Remove whitespace from before and after words.
    text = file.read().split()
    n = 0

    for a_part in text:
        word = Words(a_part)
        check_word(word, word_array)
        # Save word in word array.
        word_array[n] = word.content.lower()
        # Add words continuesly, make sure it does not go below zero.
        if n == (NUMBER_OF_WORDS - 1):
            n = 0
        else:
            n += 1
        Window.display_word(application, word)
    file.close()
    return


# Creating the GUI for the user.
class Window(Frame):

    # Constructor.
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")
        self.parent = parent
        self.parent.title("Word filter checker program for repeating words.")
        self.show_widget()
        return

    # Creation widget.
    def show_widget(self):
        welcome_frame = Frame()
        welcome_text = ("Repeating words checker program. Black belt edition.")
        welcome_label = Label(welcome_frame,
                              text=welcome_text,
                              width=10,
                              height=1)

        welcome_label.pack(pady=2, padx=2, fill=BOTH, expand=1)
        welcome_frame.pack(fill=BOTH)

        large_frame = Frame()
        left_frame = Frame(large_frame, borderwidth=10, relief=GROOVE)
        scrollbar = Scrollbar(left_frame)

        self.text = Text(left_frame,
                         height=25,
                         width=40,
                         state=DISABLED,
                         wrap=WORD,
                         yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=3)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        right_frame = Frame(large_frame, pady=10, padx=10)

        exception_frame = Frame(right_frame)
        self.exception_entry = Entry(exception_frame)
        self.exception_entry.pack(side=RIGHT, padx=3)
        exception_button = Button(exception_frame, text="Add the word to " +
        "exception list",
                                  command=self.read_word)
        exception_button.pack(side=LEFT)
        exception_frame.pack(side=TOP)

        select_frame = Frame(right_frame)
        self.selected = IntVar(select_frame)
        self.word_exception_selected = Checkbutton(select_frame,
                                                   text="Save word permanently",
                                                   variable=self.selected)
        # e = east
        self.word_exception_selected.pack(anchor="e")
        select_frame.pack(side=TOP)
        self.exception_label = Label(right_frame, text="")
        self.exception_label.pack(side=TOP)

        file_frame = Frame(right_frame)

        open_button = Button(file_frame,
                             text="Open file",
                             command=self.open_file)
        open_button.pack(side=LEFT)
        self.check_it_button = Button(file_frame,
                                      text="Check it",
                                      command=self.begin,
                                      state=DISABLED)
        self.check_it_button.pack(side=LEFT)
        file_frame.pack(side=TOP)

        exit_frame = Frame(right_frame)
        exit_button = Button(exit_frame,
                             text="Exit program",
                             command=root.destroy)
        exit_button.pack(padx=15)
        exit_frame.pack(side=BOTTOM, fill="y", anchor="e")

        right_frame.pack(side=LEFT, fill="y")

        large_frame.pack(fill="both", expand=True, padx=8, pady=8)
        return

    # Open the file.
    def open_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("Text files",
                                                                "*.txt")])
        self.check_it_button.config(state=NORMAL)
        return

    # Read in from entry and print out status message.
    def read_word(self):
        word = self.exception_entry.get().strip().lower()

        if word == "":
            self.exception_label.config(fg="red",
                                        text="Nothing in the field.")
        elif word_in_array(word, exception_array):
            self.exception_label.config(fg="red",
                                        text="Word already saved.")
        else:
            save_exception(word, self.selected.get())
            self.exception_label.config(fg="green", text="Word saved.")
        self.word_exception_selected.deselect()
        self.exception_entry.delete(0, END)
        return

    # Begin checking text from file.
    def begin(self):
        self.exception_label.config(text="")
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.config(state=DISABLED)
        check_text(self.file_name)
        return

    # Write Word-object to user with signs, ...if any are found.
    # Param: Word-object.
    def display_word(self, word):
        self.text.tag_config("Selected", background="pink")
        self.text.config(state=NORMAL)
        if word.selected:
            self.text.insert(END, word.content, "Selected")
        else:
            self.text.insert(END, word.content)
        self.text.insert(END, word.sign+" ")
        self.text.config(state=DISABLED)
        return


# Main program start.
exception_array = create_array(EXCEPTION_FILE)
root = Tk()
root.resizable(0, 0)
application = Window(root)
root.mainloop()
