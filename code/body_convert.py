#!/usr/bin/python
# -*- coding: utf-8 -*-
#this is the "so many labels are stupid" version
import sys
import csv
from common_annot import time2sec, safeopen_table, report
from os.path import exists, join as opj
from os import mkdir

columnheaders = ("start", "end", "actor", "recipient", "bodypart_actor", "bodypart_recipient", "label", "intensity_of_body_contact", "valence_actor", "valence_recipient", "intention", "audio_information")




people = {
    "oldman": "OLDMAN",
    "oldmen": "OLDMEN",
    "oldwoman": "OLDWOMAN",
    "man": "MEN",
    "woman": "WOMAN",
    "men": "MEN",
    "wen": "WOMEN",
    "boy": "BOY",
    "gil": "GIRL",
    "children": "CHILDREN",
    "jc": "JENNY",
    "fg": "FORREST",
    "dt": "DAN",
    "bb": "BUBBA",
    "mg": "MRS. GUMP",
    "olderboys": "OLDERBOYS",
    "crowd": "CROWD",
    "": "",
}

bodyparts = {
    "hand": "HAND_ARM",
    "schulter": "BODY",
    "kopf": "HEAD_NECK",
    "gesicht": "HEAD_NECK",
    "nacken": "HEAD_NECK",
    "hals": "HEAD_NECK",
    "brust": "BODY",
    "arm": "HAND_ARM",
    "bauch": "BODY",
    "ruecken": "BODY",
    "huefte": "BODY",
    "gesaess": "BODY",
    "schoss": "LEGS_FEET",
    "bein": "LEGS_FEET",
    "fuss": "LEGS_FEET",
    "haende": "HAND_ARM",
    "schultern": "BODY",    
    "arme": "HAND_ARM",
    "beine": "LEGS_FEET",   
    "fuese": "LEGS_FEET",
    "": "",
    
}
# this shows up in the annotation but doesn't work    "gesaeá": "BODY",

touches = {
    "abt": "SCAN",
    "ans": "NUDGE",
    "remp": "JOSTLE",
    "ein": "HOOK_ARM",
    "arm": "ARM_AROUND_SHOULDER",
    "aus": "UNDRESS_SOMEONE",
    "fes": "HOLD",
    "fueh": "LEAD",
    "hah": "HOLD_HANDS",
    "haes": "SHAKE_HANDS",
    "klei": "FIX CLOTHING",
    "klop": "TAP",
    "lag": "CHANGE_POSITION",
    "nah": "NESTLE",
    "fei": "SMACK",
    "lie": "LAY_ON_SOMEBODY",
    "zie": "PULL_SOMEBODY",
    "rin": "WRESTLE",
    "weg": "PUSH_AWAY",
    "hit": "HIT",
    "sch": "CUDDLE",
    "sb": "BRUSH PAST",
    "tac": "TACKLE",
    "tae": "PAT",
    "tanz": "DANCE",
    "tra": "CARRY",
    "hug": "HUG",
    "": "",    
}


intensity = {
    "str": "1",
    "wea": "0",  
    "" : "",
}

valence = {
    "spos": "POSITIVE",
    "pos": "POSITIVE",    
    "neg": "NEGATIVE",
    "sneg": "NEGATIVE",  
    "" : "",
}

intention = {
    "ja" : "1",
    "nein": "0",
    "" : "",
}

audinfo = {
    "narr": "NARRATION",
    "aud": "AUDITORY",
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
