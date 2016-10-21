#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is the "so many labels are stupid" version
#it uses the data from the original convert script (that's the data in release form) and simplifies the labels)
import sys
import csv
from common_annot import time2sec, safeopen_table, report
from os.path import exists, join as opj
from os import mkdir

columnheaders = ("start", "end", "actor", "recipient", "bodypart_actor", "bodypart_recipient", "label", "intensity_of_body_contact", "valence_actor", "valence_recipient", "intention", "audio_information")




people = {
    "OLDMAN": "OLDMAN",
    "OLDMEN": "OLDMEN",
    "OLDWOMAN": "OLDWOMAN",
    "MEN": "MEN",
    "WOMAN": "WOMAN",
    "MEN": "MEN",
    "WOMEN": "WOMEN",
    "BOY": "BOY",
    "GIRL": "GIRL",
    "CHILDREN": "CHILDREN",
    "JENNY": "JENNY",
    "FORREST": "FORREST",
    "DAN": "DAN",
    "BUBBA": "BUBBA",
    "MRS_GUMP": "MRS_GUMP",
    "OLDERBOYS": "OLDERBOYS",
    "CROWD": "CROWD",
    "": "",
}

bodyparts = {
    "HAND": "HAND",
    "SHOULDER": "BODY",
    "HEAD": "HEAD_NECK",
    "FACE": "FACE",
    "NAPE": "HEAD_NECK",
    "NECK": "HEAD_NECK",
    "CHEST": "BODY",
    "ARM": "BODY",
    "ABDOMEN": "BODY",
    "BACK": "BODY",
    "HIP": "BODY",
    "BUTTOCKS": "BODY",
    "LAP": "LEGS_FEET",
    "LEG": "LEGS_FEET",
    "FOOT": "LEGS_FEET",
    "": "",
    
}
# this shows up in the annotation but doesn't work    "gesaeá": "BODY",

touches = {
    "SCAN": "SCAN",
    "NUDGE": "NUDGE",
    "JOSTLE": "JOSTLE",
    "HOOK_ARM": "HOOK_ARM",
    "ARM_AROUND_SHOULDER": "ARM_AROUND_SHOULDER",
    "UNDRESS_SOMEONE": "UNDRESS_SOMEONE",
    "HOLD": "HOLD",
    "LEAD": "LEAD",
    "HOLD_HANDS": "HOLD_HANDS",
    "SHAKE_HANDS": "SHAKE_HANDS",
    "FIX_CLOTHING": "FIX_CLOTHING",
    "TAP": "TAP",
    "CHANGE_POSITION": "CHANGE_POSITION",
    "NESTLE": "NESTLE",
    "SMACK": "SMACK",
    "LAY_ON_SOMEBODY": "LAY_ON_SOMEBODY",
    "PULL_SOMEBODY": "PULL_SOMEBODY",
    "WRESTLE": "WRESTLE",
    "PUSH_AWAY": "PUSH_AWAY",
    "HIT": "HIT",
    "CUDDLE": "CUDDLE",
    "BRUSH_PAST": "BRUSH_PAST",
    "TACKLE": "TACKLE",
    "PAT": "PAT",
    "DANCE": "DANCE",
    "CARRY": "CARRY",
    "HUG": "HUG",
    "": "",    
}


intensity = {
    "1": "1",
    "0": "0",  
    "" : "",
}

valence = {
    "STRONG_POSITIVE": "POSITIVE",
    "POSITIVE": "POSITIVE",    
    "NEGATIVE": "NEGATIVE",
    "STRONG_NEGATIVE": "NEGATIVE",  
    "" : "",
}

intention = {
    "1" : "1",
    "0": "0",
    "" : "",
}

audinfo = {
    "NARRATION": "NARRATION",
    "AUDITORY": "AUDITORY",
    "": "",

}

def convert(fname, id_):
    print("Parsing {0} -> {1}".format(fname, id_))
    csvreader = safeopen_table(fname)
    #MS opj: set new table directory
    tdir = opj(".", "compact_data")
    #MS check if directory exists; make it otherwise
    if not exists(tdir) :   
        mkdir(tdir)

    #MS initialize writing
    csvwriter = csv.writer(open(opj(tdir, "obs{0}.csv".format(id_)), "w"))

    # skip header
    if hasattr(csvreader, "next"):
          csvreader.next()
    else:
          csvreader.__next__()

    #MS write columne headers
    csvwriter.writerow(columnheaders)
#macht die zeiten ordentlich (nochma sicher stellen ob das Frames oder Sekunden sind)
    for i, ev in enumerate(csvreader):
        # this throws out lines with missing time stamps. 2 over all observers
       if not ev[1] == "": 
        # convert everything to seconds
            start = time2sec(ev[0], i)
            end = time2sec(ev[1], i, allow_empty=True)

        # XXX TODO
        # shift the given shot marker by 2 frames, Advene issue, NEEDS VERIFICATION
        # start1 -= .08
# HIER WERDEN DIE NEUEN ZEILEN GESCHRIEBEN EINTRAG FuR EINTRAG AUF REIHENFOLGE ACHTEN        
            csvwriter.writerow((
                # shot --- excluded
                # start time
                "{0:.2f}".format(start),
                # end time
                "{0:.2f}".format(end),
                # actor
                " ".join([people[d] for d in ev[2].split() if d in people.keys()]),
                # recpient
                " ".join([people[d] for d in ev[3].split() if d in people.keys()]),
                # bodypart actor
                " ".join([bodyparts[d] for d in ev[4].split() if d in bodyparts.keys()]),
                # bodypart recipient
                " ".join([bodyparts[d] for d in ev[5].split() if d in bodyparts.keys()]),
                # label
                " ".join([touches[d] for d in ev[6].split() if d in touches.keys()]),
                # intensity
                " ".join([intensity[d] for d in ev[7].split() if d in intensity.keys()]),
                # valence actor
                " ".join([valence[c] for c in ev[8].split() if c in valence.keys()]),
                #valence recipient
                " ".join([valence[c] for c in ev[9].split() if c in valence.keys()]),
                #intention
                " ".join([intention[c] for c in ev[10].split() if c in intention.keys()]),
                # audio information
                " ".join([audinfo[c] for c in ev[11].split() if c in audinfo.keys()]),
                
            ))
       else:
            print("Line Skipped because of missing Timestamp")
if __name__ == "__main__":
  #  print(sys.argv[1:])
    for i in enumerate(sorted(sys.argv[1:])):
          convert(i[1], i[0] + 1)
