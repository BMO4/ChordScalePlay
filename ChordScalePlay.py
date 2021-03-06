#############################################################################################################################################################
#  ChordScalePlay.py
#
#  Author: Matt Crane
#  Date:   10/12/2018
#  Licence: GNU GPLv3.0
#
# -python program for music creation 
# -facillitates a user unaware of music theory to make music of coherent harmonic complexity
# -generates ChordScales as class ojects (families of scales and chords) 
# -chords and scales (attributes) confined to one octave to facillitate voice leading, minimal large intervallic leaps
# -maps these dynamically to qwerty keyboard
# -[a-g,z-n] select key/root note (ie c,c#,d,d# -> b)
# -[1-7] play chords of that key from degree 1-7 (one octave, various inversions, plus bass note)
# -[r-p] play melodic scale note (one octave)
# -Intkey defines intervallic structure of scale (eg T=2 semitones, S=1 semitone, major scale=[T,T,S,T,T,T]=[2,2,1,2,2,2])
# -proof of concept/s explored in python, anticipated that limitation of latency won't be overcome until implemented in compiled language eg C
#  NB: click in widget box to focus/get started!
###########################################################################################################################################################
class ChordScale:    

  def __init__(self, intkey, rt):
    self.intkey = intkey
    self.rt = rt
    self.mididiff = midi_diff(self.intkey)
    self.midinum =  list(map(lambda x: x+self.rt, self.mididiff))
    self.midinumdbl =  self.midinum + (list(map(lambda x: x+12, self.midinum)))
    self.chds = chd_gen(self.midinumdbl)
    self.oneoctscale = one_oct(self.midinum)

def midi_diff(intkey):
     
    mididiff = []
    for n in range(len(intkey)):
      if n == 0 :
        mididiff.append(intkey[0])
      else:
        mididiff.append(mididiff[n-1]+ intkey[n])
    mididiff.insert(0,0)

    return(mididiff)


def one_oct(scale):
  oneoct_scale = []
  for i in scale:
    oneoct_scale.append(60+(i%12))
  
  return(sorted(oneoct_scale))

def chd_gen(scale):
  chds = []
  for i in range(len(scale)-7):
    chds.append(one_oct(list(scale[i:i+5:2])))
  
  return(chds)

Cmajor = ChordScale([2,2,1,2,2,2], 60)
print(Cmajor.__dict__)

from tkinter import *
import pygame.midi

root = Tk()

pygame.midi.init()

print (pygame.midi.get_device_info(1))
player = pygame.midi.Output(1)
player.set_instrument(4)



KeyKeys = [ 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b', 'n' ]
ScaleKeys = [ 'r', 't', 'y', 'u', 'i', 'o', 'p' ]
ChordKeys = [ '1', '2', '3', '4', '5', '6', '7' ]

rt = 60

def key(event):  
  intkey = [2,2,1,2,2,2]
  if event.char in KeyKeys: 
    print ("key index pressed", repr(int(KeyKeys.index(event.char))))
    global rt
    rt = (60 + (int(KeyKeys.index(event.char))))
    global Scale
    Scale = ChordScale(intkey, rt)
    print(Scale.rt)

  if event.char in ChordKeys:
    chd = []
    chd = (Scale.chds[int(ChordKeys.index(event.char))])
    print(chd)
    for i in chd:
      player.note_on(i, velocity=95, channel=0)
    player.note_on(((chd[0])-24), velocity=80, channel=0)
    print((chd[0])-24)
    
      
  if event.char in ScaleKeys:
    melnote = ()
    melnote = (Scale.oneoctscale[int(ScaleKeys.index(event.char))])
    print(melnote)
    player.note_on(melnote, velocity=127, channel=0)
    
def callback(event):
    frame.focus_set()
    print ("clicked at", event.x, event.y)


frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()


