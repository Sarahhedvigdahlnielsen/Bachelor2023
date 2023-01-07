# Bachelor Experiment

# Sarah Hedvig Dahl Nielsen & Elisabet Skovgaard Vick
# Cognitive Science @ AU
# September / October 2022

# Import modules
from psychopy import visual, core, event, gui, data
import pandas as pd
import numpy as np
import glob, os, random
from itertools import combinations
import itertools

### create dialogue box for time entry
myDlg = gui.Dlg(title = "Understanding Early Human Cognition")
myDlg.addText('Participant Info')
myDlg.addField('Participant ID:')
myDlg.addField('Age:')
myDlg.addField('Gender:', choices=['female', 'male', 'other'])
myDlg.addField('Handedness:', choices=['left', 'right', 'both'])
myDlg.show()
if myDlg.OK:
    ID = myDlg.data[0]
    age = myDlg.data[1]
    gender = myDlg.data[2]
    handedness = myDlg.data[3]
else:
    core.quit()
 
# define win object
win = visual.Window(fullscr=True, color = 'white', units = 'height')

# define mouse
mouse = event.Mouse()

# define timestamp object
date = data.getDateStr()

# define clock object
stopwatch = core.Clock()

# define pandas data frame for logging
columns = ['Date','ID', 'Age', 'Gender', 'Handedness', 'Type', 'Trial', 'Rstim', 'Lstim', 'Rstim_period', 'Lstim_period', 'Rstim_site', 'Lstim_site', 'Probe' ,'Reaction_time']
DATA = pd.DataFrame(columns=columns)

# logfile directory
if not os.path.exists('logfiles'):
    os.makedirs('logfiles')
logfile_path = 'logfiles/'

# logfile name
logfile_name = "logfiles/logfile_{}_{}.csv".format(ID, date)

############ DEFINE FUNCTIONS ###################

def prepare_stim(stimuli, path_idx):
    STIMULI = []
    for stimulus in stimuli: 
        period = stimulus[path_idx]
        if '1' in stimulus or '2' in stimulus:
            site = 'diepkloof'
        elif '3' in stimulus or '4' in stimulus:
            site = 'blombos'
        STIMULI += [{
            'file': stimulus,
            'stimulus': stimulus[path_idx:-4], 
            'period': period,
            'site': site}] 
    return STIMULI

def create_trials(stimuli):
    trials = list(combinations(stimuli, 2)) # Det her er ændret fra STIMULI til stimuli
    random.shuffle(trials)
    return trials
   
def msg(txt, t):
    instructions = visual.TextStim(win, text=txt, color = 'black', height = 0.02) # create an instruction text
    instructions.draw()
    win.flip()
    core.wait(t)
    while not arrow.contains(mouse):
        if event.getKeys(['escape']):
            DATA.to_csv(logfile_name)
            core.quit()
        instructions.draw()
        arrow.draw()
        win.flip()

def show_images(trial):
    if random.sample([True, False],1)[0]:
        left = trial[0]
        right = trial[1]
    else:
        left = trial[1]
        right = trial[0]
    stim1 = visual.ImageStim(win, image = left['file'], units="pix", pos = (-300,0)) 
    stim2 = visual.ImageStim(win, image = right['file'], units="pix", pos = (300,0)) 
    stim1.draw()
    stim2.draw()
    win.flip()
    return left, right

def practice():
    stim1 = visual.ImageStim(win, image = 'practice/practice1.png', units="pix", pos = (-300,0))
    stim2 = visual.ImageStim(win, image = 'practice/practice2.png', units="pix", pos = (300,0))
    txt = visual.TextStim(win, text = instruction2, pos = [0,0.35], color = 'black', height = 0.02)
    
    while not startCircle.contains(mouse):
        if event.getKeys(['escape']):
            core.quit()
        startCircle.draw()
        txt.draw()
        win.flip()
    
    stim1.draw()
    stim2.draw()
    txt.draw()
    win.flip()
    core.wait(0.5) # Not hard coded
    
    if random.sample([True, False],1)[0]:
        circle = leftCircle
        probe = "left"
    else:
        circle = rightCircle
        probe = "right"
    
    while not circle.contains(mouse):
        if event.getKeys(['escape']):
            core.quit()
        circle.draw()
        txt.draw()
        win.flip()

############ DEFINE SHAPES ######################

startCircle = visual.Circle(
    win=win,
    units="pix",
    radius=50,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1],
    pos = (0, -300)
)

leftCircle = visual.Circle(
    win=win,
    units="pix",
    radius=50,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1],
    pos = (-300, 0)
)

rightCircle = visual.Circle(
    win=win,
    units="pix",
    radius=50,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1],
    pos = (300, 0)
)

# define arrow
arrowVert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
arrow = visual.ShapeStim(win=win, vertices=arrowVert, fillColor='black', size=400, lineColor='black', units = "pix", pos = (600,-280))

############## PREPARE STIMULI #####################

# stimulus directories
path = 'stimuli/'

# indexing where the stimulus name starts
path_idx = len(path)

# get stimulus images
stimuli = glob.glob(path + '*.png')

# prepare stimuli dictionaries
STIMULI = prepare_stim(stimuli, path_idx)

# prepare stimuli combinations
trials = create_trials(STIMULI)

################ INSTRUCTIONS #########################

# instruction texts
instruction1 = '''
Tusind tak fordi du vil deltage i "Understanding Early Human Cognition"-eksperimentet.

I løbet af forsøget vil du blive vist sort / hvide billeder af indgraveringer, der er op til 100 000 år gamle.
Objekterne, hvor indgraveringerne er lavet på, stammer fra to arkæologiske udgravninger i Sydafrika.

Hver runde starter ved, at du trykker på en sort cirkel i bunden af skærmen. 
Herefter vil der kort dukke to af de førnævnte billeder op på skærmen. Under et af disse, vil der nu dukke endnu en sort cirkel op.
Det er din opgave at trykke på DENNE cirkel så hurtigt som muligt.

Tryk på den sorte pil for at gå videre til træningsrunderne...
'''

instruction2 = '''
Her er et par eksempler på en runde i eksperimentet.

En runde begynder, når du trykker på den sorte cirkel i midten. Herefter vil der kort blive vist to billeder på skærmen.
Under et af disse billeder, vil der dukke en sort cirkel op. Din opgave er at trykke på DENNE cirkel så hurtigt som muligt. 
'''

instruction3 = '''
Godt gået! Nu er du klar til at starte eksperimentet.

Eksperimentet består af {} runder. Der vil være nogle pauser i løbet af eksperimentet.

Tryk på den sorte pil for at starte... 
'''.format(len(trials))

pause = '''
Nu er det tid til en pause. Tryk på den sorte pil for at fortsætte...
'''

goodbye = '''
Eksperimentet er nu færdigt. Tusind tak for din deltagelse!

Tryk på den sorte pil for at afslutte.
'''


########### RUN EXPERIMENT ##############

msg(instruction1, 5)
practice()
practice()
practice()
msg(instruction3, 3)

# trial counter
count = 1

type = "stimulus"
for trial in trials:
    if count in [69, 138, 207]:
        msg(pause, 2)

    while not startCircle.contains(mouse):
        if event.getKeys(['escape']):
            DATA.to_csv(logfile_name)
            core.quit()
        startCircle.draw()
        win.flip()
        
    left, right = show_images(trial)
        
    core.wait(0.5)
        
    if random.sample([True, False],1)[0]:
        circle = leftCircle
        probe = "left"
    else:
        circle = rightCircle
        probe = "right"
    
    stopwatch.reset()
    
    while not circle.contains(mouse):
        if event.getKeys(['escape']):
            DATA.to_csv(logfile_name)
            core.quit()
        circle.draw()
        win.flip()
    
    reaction_time = stopwatch.getTime()
    
    DATA = DATA.append({
        'Date': date,
        'ID': ID, 
        'Age': age, 
        'Gender': gender,
        'Handedness': handedness,
        'Type': type,
        'Trial': count, 
        'Rstim': right['stimulus'],
        'Lstim': left['stimulus'],
        'Rstim_period': right['period'],
        'Lstim_period': left['period'],
        'Rstim_site': right['site'],
        'Lstim_site': left['site'],
        'Probe': probe,
        'Reaction_time': reaction_time
        }, ignore_index=True)
    count += 1
    
    win.flip()
    core.wait(1)

DATA.to_csv(logfile_name)

msg(goodbye, 1)