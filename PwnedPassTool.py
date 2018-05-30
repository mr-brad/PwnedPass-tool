#!/usr/bin/env python3

###Imports
#GUI dependencies
import tkinter as tk
from tkinter import ttk
#Other dependencies
import webbrowser
import hashlib
import urllib.request

###### Interface Strings
# Strings of text used in the interface - separated out for easy maintainence
explain_tool = (
    "This tool demonstrates k-Anonymity in Troy Hunt's Pwned Passwords service."
)
explain_manual_api1 = (
    "The API accepts a /GET request including the prefix (first 5 letters) of your hash.\n"
    "Copy this into a browser or hit the Open button."
)
explain_manual_api2 = (
    "The service replies with known hashes that match the first 5 characters.\n"
    "You then search the list for your hash's suffix."
)
explain_auto_api = (
    "The following button calls the API shown above.\n"
    "If a matching hash exists, it will tell you how often."
)
match_found = (
    "Bad news! This password appears %s time(s) in password dumps."
)
no_match = (
    "Not found. Good news! This password has not been seen."
)
api_intro = "The current hash is: "
pwned_api = "https://api.pwnedpasswords.com/range/"
user_agent_string = 'Python Pwned-Pass educational tool to demo k-anonymity.'

###Tools and Functions
def update_fields(a=0, b=0, c=0):
    # the trace function passes in 3 unneeded variables - assigning but not using
    ## 1 - Grab updated password from entry field stringvar, hash it and use to set the hash stringvar
    pw = SV_pswd.get().encode('utf-8')
    hashed_password = hashlib.sha1(pw).hexdigest().upper()
    SV_hashed_pw.set(hashed_password)
    ## 2 Update truncated hashes
    SV_pwned_api.set(pwned_api + (hashed_password[0:5]))    # API needs prefix
    SV_hash_suffix.set(hashed_password[5:])                 # Lookup needs suffix
    ## 3 Turn on call api button - both buttons start as off
    if call_api_btn.instate(['disabled']):
        call_api_btn.state(['!disabled'])
        man_api_btn.state(['!disabled'])
    ## 4 Empty the Result field
    SV_pwned_op.set("")

def hide_pass_field():
    '''Toggle password obfuscation'''
    if BV_hide_my_pass.get() == True:
        pswd_entered.config(show = '*') # hide password field with *s
    else:
        pswd_entered.config(show = '')  # unhide password field

def test_pass():
    '''Sends hash prefix to site. Pushes results to SV_Pwned field.'''
    #Prepare variables
    api_url = SV_pwned_api.get()
    target_hash_suffix = SV_hash_suffix.get()
    #Make request
    req = urllib.request.Request(api_url)
    req.add_header('User-Agent', user_agent_string)
    #Check for errors
    try:
        with urllib.request.urlopen(req) as url:
            hits = url.read().decode()
    except urllib.error.URLError as e:
        SV_pwned_op.set(e.reason)
    #Read through lines returned, split at the colon, if hash suffix matches, return number of hits
    for each_line in hits.splitlines():
        this_hash, no_of_hits = each_line.split(':')
        if this_hash == target_hash_suffix:
            SV_pwned_op.set(match_found % no_of_hits)
            return    
    #If we get here, no matches were found
    SV_pwned_op.set(no_match)

#Opens URL in default browser
def open_url(url):
    '''Opens a given url.'''
    webbrowser.open_new(url)
#Built in links
def clicked_k_anon():
    open_url(r"https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/")
def clicked_sha():
    open_url(r"https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/#theyrestillsha1hashedbutwithsomejunkremoved")
def clicked_open_api_url():
    open_url(SV_pwned_api.get())


############################
## Add Root Window
win = tk.Tk()
win.title('Pwned Password Demo')
# Link Style for all hyperlinks
link_style = ttk.Style()
link_style.configure('link.TLabel', foreground='#44AADD')
link_style.map("link.TLabel",
    foreground=[('hover','#99CCEE')],
    )
# String Variables - TK uses these as tracked variables to display
SV_pswd = tk.StringVar()            # The password currently entered
SV_hashed_pw = tk.StringVar()       # The SHA1 hash of this password
SV_pwned_api = tk.StringVar()       # The link to hit to call the API (url/hash_prefix)
SV_hash_suffix = tk.StringVar()     # The hash suffix to be found in returned list
SV_pwned_op = tk.StringVar()        # The output message of a check
BV_hide_my_pass = tk.BooleanVar()   # Stores password obfuscation choice

#############################
# Main Box - contains all tools
main_box = ttk.LabelFrame(win, text="k-Anonymity Demo")
main_box.grid(column=0,row=0, padx=8, pady=8)
ttk.Label(main_box, text=explain_tool).grid(column=0, row=0, padx=8, sticky=tk.W)
ttk.Button(main_box, text="What is k-Anonymity?", style="link.TLabel", command=clicked_k_anon).grid(column=0, row=1, padx=8, sticky=tk.W)

##########
## Top Box - contains live hashing part
sha_box = ttk.LabelFrame(main_box, text = "SHA1 Hashing")
sha_box.grid(column=0, row=2, padx=8, pady=8, sticky=tk.EW)
ttk.Label(sha_box, text="This hashes whatever you enter using SHA1.").pack(anchor="center") #Pack easier for centring these elements
## Password field
ttk.Button(sha_box, text="Isn't SHA1 broken though?", style="link.TLabel", command=clicked_sha).pack(anchor="center")
ttk.Label(sha_box, text="Enter Password to be Tested").pack(anchor="center")
pswd_entered = ttk.Entry(sha_box, show='*', width=30, textvariable=SV_pswd)
pswd_entered.pack(anchor="center")
pswd_entered.focus()
SV_pswd.trace_add("write", update_fields)
## Obfuscation toggle - on by default
hide_pass = tk.Checkbutton(sha_box, text='Hide my Password', variable=BV_hide_my_pass, command=hide_pass_field)
hide_pass.select()
hide_pass.pack(anchor="center")
## Hash output
op_box = ttk.LabelFrame(sha_box, text = "SHA1 Hash of Entered Password")
op_box.pack(anchor="center", pady=8)
ttk.Label(op_box, width=50, anchor="center", textvariable=SV_hashed_pw).pack(anchor="center", pady=6)
## Top box ends

##########
## Middle box - contains API info and link
## Manual API call box
man_api = ttk.LabelFrame(main_box, text = "Manual API call")
man_api.grid(column=0, row=3, padx=8, pady=8, sticky=tk.EW)
man_api.grid_columnconfigure(0,weight=1)
## Explanation
ttk.Label(man_api, anchor="center", text=explain_manual_api1).grid(column=0, row=0, padx=20,sticky=tk.EW)
api_callout = ttk.Entry(man_api, width=44, textvariable=SV_pwned_api, state='readonly')
api_callout.grid(column=0, row=1, padx=20, pady=6)
ttk.Label(man_api, anchor="center", text=explain_manual_api2).grid(column=0, row=2, padx=20, sticky=tk.EW)
## Hash Suffix output
suffix_box = ttk.LabelFrame(man_api, text = "Look for this Suffix")
suffix_box.grid(column=0,row=3, pady=8)
ttk.Label(suffix_box, width=40, anchor="center", textvariable=SV_hash_suffix).pack(anchor="center", pady=2, padx=6)
## Browser call button
man_api_btn = ttk.Button(man_api,text="Open in Browser", command=clicked_open_api_url)
man_api_btn.grid(column=0, row=4, pady=8)
man_api_btn.state(['disabled'])
## Middle box ends

##########
## Bottom Box - contains tast button to call API
## Call API button
auto_api = ttk.LabelFrame(main_box, text = "Automated API call")
auto_api.grid(column=0, row=4, padx=8, pady=4, sticky=tk.EW)
auto_api.grid_columnconfigure(0,weight=1)
## Text
ttk.Label(auto_api, anchor="center", text=explain_auto_api).grid(column=0, row=0, padx=20, sticky=tk.EW)
## Button
call_api_btn = ttk.Button(auto_api,text="Test Password", command=test_pass)
call_api_btn.grid(column=0, row=1, pady=8)
call_api_btn.state(['disabled'])
## Output
reply_box = ttk.LabelFrame(auto_api, text = "Your Result")
reply_box.grid(column=0,row=2, pady=20)
ttk.Label(reply_box, width=62, anchor="center", textvariable=SV_pwned_op).pack(anchor="center", pady=2, padx=6)
## Bottom box ends
# Main box ends


# Window display loop
win.resizable(False, False)
win.mainloop()