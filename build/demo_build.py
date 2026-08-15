#!/usr/bin/env python3
"""Build demo.html — the blank tracker with a short worked oneshot in it."""
import os
from pathlib import Path
# Repo-relative paths. Override the tracker source with TABLE_AID_SOURCE.
ROOT = Path(__file__).resolve().parent.parent
SOURCE_TRACKER = Path(os.environ.get(
    'TABLE_AID_SOURCE', ROOT.parent / 'abyss_tracker.html'))

import io, json, base64, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from demo_art import PLATES

def durl(k):
    return 'data:image/svg+xml;base64,' + base64.b64encode(PLATES[k].encode()).decode()

# ---------------------------------------------------------------- maps
def M(rows):
    w = max(len(r) for r in rows)
    out = [r.ljust(w, '.') for r in rows]
    assert len(set(len(r) for r in out)) == 1
    return out

MAP1 = M([
 "##################",
 "#................#",
 "#..o....o....o...#",
 "#................#",
 "#..^^^....^^^....#",
 "#................#",
 "#~~~~~~....~~~~~~#",
 "#................#",
 "#..o....o....o...#",
 "#................#",
 "#...............D#",
 "##################"])

MAP2 = M([
 "################",
 "#..............#",
 "#..~~~~~~~~~...#",
 "#..~~~~~~~~~.o.#",
 "#..~~~~~~~~~...#",
 "#....s.....s...#",
 "#..............#",
 "#o....^^^.....o#",
 "#..............#",
 "#..............#",
 "#.............D#",
 "################"])

MAP3 = M([
 "##################",
 "#................#",
 "#..T.........o...#",
 "#................#",
 "#..~~~~~~~~~~~~..#",
 "#..~~~~~~~~~~~~..#",
 "#..~~~~~~~~~~~~..#",
 "#..~~~~~~~~~~~~..#",
 "#....s........s..#",
 "#................#",
 "#..o..........o..#",
 "#..^^^....^^^....#",
 "#...............D#",
 "##################"])

# ---------------------------------------------------------------- creatures
MON = [
{"n":"Bog Scarecrow","t":"Small Construct, Unaligned","cr":"1/2","xp":100,
 "ac":13,"hp":27,"hd":"5d8+5","dex":1,"conSv":3,"sp":"30 ft.","ab":[14,12,13,4,10,5],
 "grp":"Fenwork","side":"foe",
 "lines":["<span class='k'>Saves</span> Con +3 &middot; <span class='k'>PP</span> 10 &middot; <span class='k'>Darkvision</span> 60 ft.",
   "<span class='k'>Straw and Salt.</span> Immune to poison and to being Poisoned. <b>Vulnerable to fire</b> &mdash; and the party will work that out fast.",
   "<span class='k'>False Appearance.</span> While it stays still it is indistinguishable from an ordinary scarecrow.",
   "<span class='k'>Multiattack.</span> Two Claws.",
   "<span class='k'>Claw.</span> +4, reach 5 ft, 1d6+2 slashing.",
   "<span class='k'>Terrifying Glare.</span> One creature within 30 ft that can see it: DC 11 Wisdom save or Frightened until the end of its next turn."],
 "trig":{"combat":[{"n":"They are not moving yet","w":"All four stand exactly where the field says they should. Nothing happens until someone touches the fence line, crosses the ditch, or attacks. Let the players decide to start this fight.","k":"rem"}]}},

{"n":"Fen Hound","t":"Medium Beast, Unaligned","cr":"1","xp":200,
 "ac":13,"hp":26,"hd":"4d8+8","dex":2,"conSv":4,"sp":"40 ft., swim 30 ft.","ab":[15,14,15,3,12,6],
 "grp":"The Fen","side":"foe",
 "lines":["<span class='k'>Saves</span> Con +4 &middot; <span class='k'>Skills</span> Perception +3, Stealth +4 &middot; <span class='k'>PP</span> 13",
   "<span class='k'>Pack Tactics.</span> Advantage on an attack roll if an ally is within 5 ft of the target and not Incapacitated.",
   "<span class='k'>Keen Smell.</span> Advantage on Perception checks that rely on smell &mdash; it will find anyone hiding in the reeds.",
   "<span class='k'>Bite.</span> +4, reach 5 ft, 1d8+2 piercing, and the target makes a DC 12 Strength save or is knocked Prone."],
 "ai":True,"aiOk":False,
 "aiNote":"Statted at CR 1 — your notes say 'something in the reeds that hunts in twos', so the name and every number here are mine."},

{"n":"Drowned Miller","t":"Medium Undead, Neutral Evil","cr":"2","xp":450,
 "ac":12,"hp":45,"hd":"7d8+14","dex":1,"conSv":4,"sp":"25 ft., swim 30 ft.","ab":[16,12,15,8,10,6],
 "grp":"The Mill","side":"foe",
 "lines":["<span class='k'>Saves</span> Con +4 &middot; <span class='k'>PP</span> 10 &middot; <span class='k'>Darkvision</span> 60 ft.",
   "<span class='k'>Waterlogged.</span> Water is not difficult terrain for it, and it can hold a creature under without needing to breathe.",
   "<span class='k'>Multiattack.</span> Two Slams.",
   "<span class='k'>Slam.</span> +5, reach 5 ft, 1d8+3 bludgeoning plus 1d4 cold.",
   "<span class='k'>Drag Under.</span> If both Slams hit the same creature, that creature makes a DC 13 Strength save or is Grappled (escape DC 13) and pulled 10 ft toward the water."],
 "kit":{"dc":11,"slots":{"1":2},
   "spells":[{"n":"Ray of Frost","lv":0,"t":"Ranged attack &middot; 60 ft","d":"A beam of cold. Damage, and the target's speed drops by 10 ft until the start of your next turn."},
             {"n":"Fog Cloud","lv":1,"t":"Concentration &middot; 20-ft sphere","d":"A bank of fog that heavily obscures everything inside it. It uses this to separate the party, not to hide."}],
   "uses":[{"n":"Cold Grip","max":1,"note":"Once per fight: as a bonus action after a Slam hits, the target is also Restrained until the end of its next turn (escape DC 13)."}]}},

{"n":"Old Grist","t":"Large Fey, Neutral Evil","cr":"5","xp":1800,
 "ac":16,"hp":95,"hd":"10d10+40","dex":2,"conSv":7,"sp":"30 ft., swim 40 ft.","ab":[18,14,18,13,15,12],
 "grp":"The Mill","side":"foe","legRes":2,"legAct":3,
 "lines":["<span class='k'>Saves</span> Con +7, Wis +5 &middot; <span class='k'>Skills</span> Deception +4, Perception +5 &middot; <span class='k'>PP</span> 15",
   "<span class='k'>Millstone Grip.</span> A creature hit by Grind is Grappled (escape DC 15). She can only hold one at a time, and she holds it <b>under the water</b>.",
   "<span class='k'>Legendary Resistance (2/Day).</span> When she fails a save, she may choose to succeed instead.",
   "<span class='k'>Multiattack.</span> One Grind and one Fen Chill.",
   "<span class='k'>Grind.</span> +7, reach 10 ft, 2d8+4 bludgeoning.",
   "<span class='k'>Fen Chill.</span> +7, reach 5 ft, 2d6+4 cold, and the target's speed drops 10 ft until the end of its next turn.",
   "<span class='k'>Legendary Actions (3/turn).</span> <b>Wade</b> &mdash; move half speed through water without provoking. <b>Sluice</b> (costs 2) &mdash; the wheel surges: every creature in the water makes a DC 15 Strength save or is moved 15 ft along the race. <b>Whisper</b> &mdash; she says one true thing about a character in their own parent's voice; DC 13 Wisdom save or Frightened of her until the end of their next turn."],
 "kit":{"dc":14,"slots":{"1":3,"2":2},
   "spells":[{"n":"Ray of Frost","lv":0,"t":"Ranged attack &middot; 60 ft","d":"Cold damage and the target slows by 10 ft."},
             {"n":"Fog Cloud","lv":1,"t":"Concentration &middot; 20-ft sphere","d":"Heavy obscurement. She uses it to take someone out of sight and drown them quietly."},
             {"n":"Hold Person","lv":2,"t":"Concentration &middot; Wis save","d":"One humanoid is Paralyzed while she concentrates, with a save at the end of each of its turns."},
             {"n":"Misty Step","lv":2,"per":2,"t":"Bonus action &middot; 2/day","d":"She blinks 30 ft to a space she can see. Always back into the water."}],
   "uses":[{"n":"Call the Race","max":1,"note":"Once per fight, as an action: the sluice opens and the whole wheelhouse floor becomes waist-deep. Difficult terrain for everyone but her, and the Damp clock starts running."}]},
 "trig":{"combat":[{"n":"She starts under the water","w":"Nobody sees her until she acts. Roll her initiative but do not put a model down until her first turn — she comes up out of the race behind whoever is nearest the wheel.","k":"rem"},
                   {"n":"The sluice lever is on the north wall","w":"A DC 13 Strength (Athletics) check closes the gate. That switches off her regeneration for good. Wick knows where the lever is and will point at it if anyone asks him.","k":"rem"}],
         "turn":[{"n":"Millrace Renewal","w":"Regains 8 hit points at the start of her turn while any part of her is in running water. Closing the sluice gate ends this.","k":"auto","heal":8}]}},

{"n":"Wick","t":"Small Humanoid (child), Neutral Good","cr":"1/8","xp":25,
 "ac":12,"hp":11,"hd":"2d6+2","dex":2,"conSv":1,"sp":"30 ft.","ab":[8,14,12,11,13,12],
 "grp":"Ashfen","side":"ally",
 "lines":["<span class='k'>Skills</span> Stealth +4, Perception +3 &middot; <span class='k'>PP</span> 13",
   "<span class='k'>He is nine.</span> He is not a combatant and will not fight. If a fight starts, he hides.",
   "<span class='k'>Knows the mill.</span> Where the sluice lever is, which boards are rotten, and that his father worked nights.",
   "<span class='k'>Will not leave.</span> He will not go back to the village while his father is still down there, whatever anyone says."]},

{"n":"Sister Halloway","t":"Medium Humanoid, Lawful Good","cr":"2","xp":450,
 "ac":16,"hp":33,"hd":"6d8+6","dex":0,"conSv":3,"sp":"30 ft.","ab":[12,10,13,12,16,13],
 "grp":"Ashfen","side":"ally",
 "lines":["<span class='k'>Saves</span> Wis +5 &middot; <span class='k'>Skills</span> Insight +5, Medicine +5 &middot; <span class='k'>PP</span> 15",
   "<span class='k'>Mace.</span> +4, reach 5 ft, 1d6+2 bludgeoning. She is not good at this and knows it.",
   "<span class='k'>She will run out.</span> Five spell slots, and then she is a woman with a mace. Play her generously early and let the party feel it when she is empty."],
 "kit":{"dc":13,"slots":{"1":3,"2":2},
   "spells":[{"n":"Sacred Flame","lv":0,"t":"Dex save &middot; 60 ft","d":"Radiant damage, no cover allowed. Her reliable option once the slots are gone."},
             {"n":"Cure Wounds","lv":1,"t":"Touch","d":"Restores hit points; more for a higher slot."},
             {"n":"Bless","lv":1,"t":"Concentration &middot; 1 min","d":"Three creatures add 1d4 to attack rolls and saving throws."},
             {"n":"Lesser Restoration","lv":2,"t":"Touch","d":"Ends one disease or one condition &mdash; here, one level of the Damp."},
             {"n":"Spiritual Weapon","lv":2,"t":"Bonus action &middot; 1 min","d":"A floating weapon she can swing as a bonus action each turn."}],
   "uses":[{"n":"Channel Divinity: Turn Undead","max":1,"note":"DC 13 Wisdom save or the undead is Frightened and must move away for 1 minute. This works on the Drowned Millers and it is her best round."}]}},
]

# ---------------------------------------------------------------- encounters
ENC = [
{"n":"The scarecrow field","loc":"Ashfen · the drowned barley, dusk",
 "note":"They do not move until the party gives them a reason. Fire is the answer and the field is soaked — let someone try anyway. The ditch is chest-deep water; anyone who ends a turn in it starts the Damp clock.",
 "m":[["Bog Scarecrow",4],["Fen Hound",2]],
 "map":{"t":"The drowned barley","scale":"18 x 12 squares · 90 ft x 60 ft",
   "draw":"A flat field with two ditches of standing water running across it, fence posts in three rows, and churned mud between them. The party comes in through the gate at the bottom right.",
   "rows":MAP1,
   "tok":[{"x":3,"y":2,"l":"S","s":"foe","n":"Scarecrow"},{"x":8,"y":2,"l":"S","s":"foe","n":"Scarecrow"},
          {"x":13,"y":2,"l":"S","s":"foe","n":"Scarecrow"},{"x":8,"y":8,"l":"S","s":"foe","n":"Scarecrow"},
          {"x":4,"y":7,"l":"H","s":"foe","n":"Fen Hound"},{"x":12,"y":7,"l":"H","s":"foe","n":"Fen Hound"},
          {"x":16,"y":10,"l":"P","s":"pc","n":"The party"}]}},

{"n":"The drowned wheel","loc":"The mill yard · first hour of the night",
 "note":"Two of them come up out of the millpond and one is already behind the party, in the water butt by the gate. Sister Halloway's Turn Undead lands here if she has followed them out.",
 "m":[["Drowned Miller",2],["Fen Hound",2]],
 "map":{"t":"The mill yard","scale":"16 x 12 squares · 80 ft x 60 ft",
   "draw":"The millpond fills the top left. Two short stairs come up out of it onto the yard. A cart and a woodpile sit in the middle as cover, the well is on the right, and the yard gate is bottom right.",
   "rows":MAP2,
   "tok":[{"x":5,"y":3,"l":"D","s":"foe","n":"Drowned Miller"},{"x":9,"y":2,"l":"D","s":"foe","n":"Drowned Miller"},
          {"x":2,"y":8,"l":"H","s":"foe","n":"Fen Hound"},{"x":13,"y":8,"l":"H","s":"foe","n":"Fen Hound"},
          {"x":14,"y":10,"l":"P","s":"pc","n":"The party"}]},
 "ai":True,"aiOk":False,
 "aiNote":"Guessed the map from 'the mill yard, the pond on one side, a cart to hide behind' — the stairs, the well and the exact layout are mine."},

{"n":"Old Grist","loc":"Inside the wheelhouse · the last twenty minutes",
 "note":"She is in the race, under the wheel, and she does not come up until her first turn. Two scarecrows come down the ladder on round two. The lever on the north wall closes the sluice and ends her regeneration — that is the fight.",
 "m":[["Old Grist",1],["Bog Scarecrow",2]],
 "map":{"t":"The wheelhouse","scale":"18 x 14 squares · 90 ft x 70 ft",
   "draw":"The millrace runs across the middle of the room, four squares deep, with the wheel turning at the left end. Two short stairs cross it. The sluice lever is on the plinth top left. Sacks and broken gearing give cover along the bottom.",
   "rows":MAP3,
   "tok":[{"x":4,"y":5,"l":"G","s":"foe","n":"Old Grist (submerged)"},
          {"x":3,"y":2,"l":"L","s":"pc","n":"Sluice lever"},
          {"x":13,"y":11,"l":"S","s":"foe","n":"Scarecrow"},{"x":6,"y":11,"l":"S","s":"foe","n":"Scarecrow"},
          {"x":16,"y":12,"l":"P","s":"pc","n":"The party"}]}},
]

# ---------------------------------------------------------------- tools
TOOLS = [{
 "id":"damp","name":"The Damp",
 "rule":"Ashfen water does not want to let go of you.",
 "trigger":"A creature that has been in the millwater makes a Constitution save when it gets out, and again for every further 10 minutes it stays in. The tier is total time in the water tonight, not time since the last save. Getting properly dry and warm clears the count — not the exhaustion.",
 "cols":["Time in the water","DC","On a failure","On a success"],
 "rows":[["Up to 10 minutes","10","1 level of Exhaustion","No effect"],
         ["10–30 minutes","13","1 Exhaustion, and roll on What the Water Says","1 Exhaustion"],
         ["Over 30 minutes","16","2 Exhaustion, and speed is halved until a long rest","1 Exhaustion"],
         ["Held under by Old Grist","—","No save. See her Millstone Grip — this is drowning, not the Damp.","—"]],
 "dcCol":1,"ability":"Constitution",
 "res":{"on":True,"amountLabel":"Minutes in the water","amount":10,"unit":10,
        "advLabel":"A fire and dry clothes within reach (advantage, one save per 20 min)","advUnit":20},
 "dtable":{"name":"What the Water Says (d6)","die":6,
   "items":["You hear your own name, from under the surface, in your own voice.",
     "Everything you are carrying is suddenly, impossibly heavy. Drop something or move at half speed.",
     "You are certain the water is warmer further down.",
     "For a moment you can see perfectly clearly underwater, and there is somebody standing on the bottom.",
     "Your lantern gutters and burns green. It gives no warmth for an hour.",
     "You are dry. Your clothes are dry, your hair is dry, and nobody else can see it."]},
 "notes":[{"t":"Getting dry","b":"A short rest by a fire clears the running count. It does not remove exhaustion — that needs a long rest, or Sister Halloway's Lesser Restoration, of which she has exactly two."},
   {"t":"Why it exists","b":"So that wading is a decision rather than free movement. Every map in this oneshot has water on it, and the players should be weighing whether to cross it or go the long way round."}]
}]

# ---------------------------------------------------------------- handouts
CARDS = [
{"id":"h_dials","name":"The strongbox lid — the puzzle","img":durl('dials'),
 "text":"Four brass dials, each stamped with a picture: a wave, a wheel, a sheaf of wheat, a moon.\n\nScratched into the lid above them, in a hand that pressed too hard:\n\n“What comes first has no hands.\nWhat comes next is turned by it.\nWhat comes third is broken by that.\nAnd what comes last is my only witness.”",
 "dm":"SOLUTION — press them in this order: WATER, WHEEL, WHEAT, MOON.\n\nWater has no hands. The wheel is turned by the water. The wheat is broken by the wheel. And the moon was his only witness, because he milled at night — which is the thing the party has not worked out yet.\n\nA wrong order: the lid spits a needle. DC 12 Dexterity save or 1d4 piercing and Poisoned for 1 minute. It will do this every time; it never locks them out.\n\nHINTS, in order of cheapness:\n• Wick, unprompted, if anyone asks about his father's hours: “He worked nights. Mam hated it.”\n• DC 12 Investigation on the mill floor: fresh grain dust only under the north window, where the moon comes in.\n• If they are properly stuck, let Sister Halloway read the rhyme aloud and stop, deliberately, on ‘my only witness’.\n\nInside: 31 gold, a deed, and the letter (the next handout)."},

{"id":"h_letter","name":"The letter in the strongbox","img":"",
 "text":"To the miller of Ashfen, greetings.\n\nThe tithe on your mill is forty-one gold and is now nine months in arrears. The Reeve is minded to be patient. The Reeve is not minded to be patient twice.\n\nYou will understand that a mill which does not pay is a mill which does not grind, and a village which does not grind is a village which moves. We would all prefer it did not come to that.\n\nYou have until the first frost.\n\n— by the hand of Corwen Vail, for the Reeve of Marchford",
 "dm":"This is the WHY. He could not pay, so he took the deal that was offered to him at the water's edge, and he has been milling at night for something that does not eat bread.\n\nIt is dated eleven months ago. The first frost was two months ago.\n\nIf a player asks what he was grinding — that is the right question, and the answer is at the bottom of the race in scene 6. Do not answer it here."},

{"id":"h_wick","name":"Wick's drawing","img":durl('drawing'),
 "text":"",
 "dm":"Give them this without comment. Wick drew it three days ago and his mother took it off the wall.\n\nIt is the mill, the wheel, and a stick figure standing inside the wheel with its arms out. Underneath, in a nine-year-old's hand: ‘dad’.\n\nHe will tell you, if asked gently, that he sees his father in the wheel most nights, and that his father waves. He does not think this is frightening. He thinks everyone is being strange about it.\n\nThis is the first hard evidence that the miller is not simply missing, and it should land about fifteen minutes before the party is ready for it.",
 "ai":True,"aiOk":False,
 "aiNote":"Invented — your notes say the boy 'knows more than he is saying' but never say what, and the party needs one concrete thing to hold before the mill."},
]

# ---------------------------------------------------------------- story
CH = [
 {"id":"c1","name":"Chapter One — Ashfen","sub":"The village, and what it will not say","open":True},
 {"id":"c2","name":"Chapter Two — The Mill","sub":"Everything the village would not say","open":True},
]

SCENES = [
{"ch":"c1","a":"0:00","b":"0:15","t":"The causeway","imgs":[{"n":"The causeway at dusk","u":durl('causeway')}],
 "note":"Cold open on the road. Get names and one sentence of why each of them is this far out.",
 "keys":["Open on the wagon, the last of the light, and a village that is four miles further than the map said.",
   "The carter will not go past the fen boundary and will not say why. He waits for his money at the stone, not in the village.",
   "★ A scarecrow in the third field has its head turned to watch the road. If a player points at it, agree with them and move on.",
   "Ask each player what their character is hoping is waiting at the end of this road. Write the answers down — the Whisper legendary action in scene 6 uses them.",
   "End the scene the moment they can hear the mill wheel. They should hear it before they see it."]},

{"ch":"c1","a":"0:15","b":"0:40","t":"Ashfen","imgs":[{"n":"Ashfen from the water","u":durl('ashfen')}],
 "note":"Three things to find here. Let them get two. The third is the one they will wish they had.",
 "keys":["The village is sixty people and every one of them is polite and none of them will discuss the mill.",
   "★ SISTER HALLOWAY at the chapel will talk. The miller has been gone eleven days. Nobody has gone to look. She is ashamed of that and says so.",
   "★ WICK, the miller's boy, is throwing stones at the water and not going home. He has a drawing (Tools → handouts). Give it to them without comment.",
   "The reeve's man came through nine months ago and again in the spring. Two people mention it and both change the subject.",
   "If they ask to see the mill, everyone finds a reason to be elsewhere. Halloway will come with them. Wick will follow whether they let him or not.",
   "Time check: leave here by 0:40 even if they have not found everything."]},

{"ch":"c1","a":"0:40","b":"0:55","t":"FIGHT: the scarecrow field","enc":"The scarecrow field",
 "note":"The only route to the mill crosses the barley. They do not move until the party does something.",
 "keys":["Four scarecrows, three fence rows, two ditches of standing water. Nothing is moving.",
   "★ Let the players start this fight. They will spend a full minute deciding, and that minute is the scene.",
   "Fire is the obvious answer and everything is soaked — let them try it, let it half-work, and give them the win for thinking of it.",
   "The hounds come out of the reeds on round two, from behind.",
   "Anyone who ends their turn in a ditch has started the Damp clock (Tools tab). Say so out loud the first time, then stop reminding them."]},

{"ch":"c2","a":"0:55","b":"1:15","t":"The mill house","imgs":[{"n":"The millpond by moonlight","u":durl('millpond')}],
 "note":"The puzzle scene. The strongbox is under the floor by the grain hopper.",
 "keys":["The house is tidy. The bed is made. There is eleven days of dust and one clean patch on the table where something was taken away.",
   "★ THE STRONGBOX — four dials and a rhyme (Tools → handouts). Answer: water, wheel, wheat, moon. A wrong order costs 1d4 and a minute of poison, never a lockout.",
   "Inside: 31 gold, the deed, and the tax letter. The letter is the why — he could not pay.",
   "Wick knows his father worked nights. He will say so unprompted if anyone asks about the man rather than the mill.",
   "The wheel is turning. Nothing is driving it. Nobody has opened the sluice in eleven days.",
   "End on someone looking out at the millpond and realising the water is moving the wrong way."]},

{"ch":"c2","a":"1:15","b":"1:35","t":"FIGHT: the drowned wheel","enc":"The drowned wheel",
 "note":"Two millers out of the pond, two hounds from the yard gate. Halloway's Turn Undead is the moment here.",
 "keys":["They come up out of the water without a sound. The first anyone knows is the cold.",
   "★ If Sister Halloway is with them, this is her scene — Turn Undead, and she is visibly terrified while she does it.",
   "The millers try to grapple and drag toward the water, not to kill. Being pulled in starts the Damp clock.",
   "One of the millers is wearing an apron with a name stitched into it, and it is not the missing man's name. There were others.",
   "Keep Wick out of it. He hides, and he watches, and he does not run."],
 "ai":True,"aiOk":False,
 "aiNote":"Filled in the key beats — your outline gives this fight one line ('the pond ones come out'), so the shape of the scene is mine."},

{"ch":"c2","a":"1:35","b":"1:55","t":"FIGHT: Old Grist","enc":"Old Grist",
 "imgs":[{"n":"Inside the wheelhouse","u":durl('wheelhouse')}],
 "note":"The boss. She is in the race and does not surface until her first turn. The sluice lever ends her regeneration.",
 "keys":["Do not put her model down at the start. Roll her initiative, say nothing, and let her come up out of the race behind whoever is closest to the wheel.",
   "★ THE FIGHT IS THE LEVER. She regains 8 HP at the start of every turn while she is in running water; a DC 13 Athletics check on the north wall closes the sluice and stops it for good. The pop-up will remind you.",
   "★ WHISPER (legendary action) — she says one true thing about a character in their parent's voice. Use the answers from scene 1. This is the payoff.",
   "Call the Race floods the whole floor once per fight. Everyone but her is in difficult terrain and the Damp clock is running for the rest of the night.",
   "The miller is at the bottom of the race, and he is still turning the wheel, and he is not going to stop.",
   "Two scarecrows come down the ladder on round two. They are a clock, not a threat — they are there to stop the party turtling.",
   "If the party is losing badly: Halloway steps into the water. That is the out, and it costs her."]},

{"ch":"c2","a":"1:55","b":"2:00","t":"Epilogue — what the water gives back",
 "note":"Five minutes. Do not extend it. End on Wick.",
 "keys":["With the sluice shut, the wheel stops for the first time in eleven days, and the whole valley notices the silence.",
   "The village comes out. Nobody apologises. Somebody has already brought bread.",
   "★ Wick asks whether his father waved. Let the player who is holding the drawing answer that. Do not answer it yourself.",
   "The deed is in the strongbox and the mill has no miller. Offer it to them and see what they say.",
   "Last image: the millpond, flat and still, and one set of footprints in the mud going down into it that nobody made tonight."]},
]

# ---------------------------------------------------------------- party
def PC(name, cls, ac, die, con, rolls, slots, feats):
    hp = 0
    for i,r in enumerate(rolls):
        hp += max(1, (die if i==0 else r) + con)
    return {"name":name,"cls":cls,"ac":ac,"hp":hp,"maxhp":hp,"temp":0,"exh":0,"layer":1,
            "ds":{"s":0,"f":0},
            "slots":[{"max":m,"used":0} for m in slots],
            "feats":[{"name":n,"max":m,"used":0} for n,m in feats],
            "hitDie":die,"conMod":con,"hpLevels":3,"perLvl":0,"flatHP":0,"maxFirst":True,
            "hpRolls":rolls}

PARTY = [
 PC("Bram Ashdown","Fighter 3 · Battle Master",18,10,3,[10,6,5],[0]*9,
    [("Second Wind",2),("Action Surge",1),("Superiority dice (d8)",4)]),
 PC("Ivy Quill","Wizard 3 · Evocation",12,6,1,[6,4,3],[4,2,0,0,0,0,0,0,0],
    [("Arcane Recovery",1),("Sculpt Spells",1)]),
 PC("Doric Vane","Cleric 3 · Life",18,8,2,[8,5,4],[4,2,0,0,0,0,0,0,0],
    [("Channel Divinity",1),("Preserve Life",1)]),
 PC("Sable","Rogue 3 · Thief",15,8,2,[8,6,3],[0]*9,
    [("Sneak Attack 2d6 — once per turn",1),("Fast Hands (bonus action)",1)]),
]

NOTES = """THE MILLER'S DEBT — a two-hour demonstration oneshot for four level-3 characters.

This file exists to show you what a filled-in Table Aid looks like. Everything in it is editable —
change a number, delete a scene, rebuild an encounter, and nothing will complain.

Things worth trying, in order:
1. Story tab — open a segment. The bullets under KEY BEATS are the summary you read mid-scene.
   Click a thumbnail under SHOW THE TABLE and it goes onto the player window.
2. Press PLAYERS in the header. A second window opens for the other screen. The initiative order
   is hidden from them until you tick the box in Tools → Player screen.
3. Encounters tab — press "Load into initiative" on The scarecrow field. Watch the start-of-combat
   pop-up fire, and note that every foe now carries a table number for your dice.
4. Initiative tab — press ◉ Area damage and drop a fireball on the field.
5. Tools tab — roll 4d6kh3, work the Damp resolver, and open the strongbox handout to see a puzzle
   with its solution attached.
6. Four things in this file are outlined in RED. That is the provenance layer: it is what Claude
   invented rather than what the author wrote. Read them, then press ✓ That's fine, or turn the
   whole layer off in ⋮ → What Claude added.

Ctrl+K jumps to anything. Ctrl+Z undoes anything."""

DATA = {
 "title":"The Miller's Debt","sub":"A demonstration",
 "theme":{"name":"verdant","mode":"dark"},
 "party":{"size":4,"level":3,"items":{},"itemPct":{}},
 "playerOrder":False,
 "chapters":CH,"scenes":SCENES,"mon":MON,"enc":ENC,"tools":TOOLS,"cards":CARDS,
}

STATE = {"round":1,"turn":0,"combatants":[],"party":PARTY,"notes":NOTES,
         "scenesDone":[False]*len(SCENES),"sceneNotes":[""]*len(SCENES),
         "sceneOpen":[True]+[False]*(len(SCENES)-1),"sceneStamp":[{} for _ in SCENES],
         "clock":{"elapsed":0,"running":False,"last":None},
         "data":DATA,"lastEnc":None,"pshow":{"kind":"map","id":None},"effects":[]}

# ---------------------------------------------------------------- write demo.html
src = io.open(ROOT/'tracker'/'table_aid_blank.html',encoding='utf-8').read()
DEMO_PANEL = """
<div class="card" id="demopanel" style="max-width:900px;margin:10px auto 0;border-left:3px solid var(--amber-d)">
  <h2 class="sec" style="color:var(--amber)">What you are looking at</h2>
  <div class="note" style="line-height:1.85">
    This is the tracker with a real two-hour oneshot already in it &mdash; <b>The Miller&rsquo;s Debt</b>,
    for four level-3 characters. It was built the way the tool is meant to be used: somebody wrote a page
    of messy adventure notes, handed them to Claude, and pasted the result in. Nothing here is a mock-up;
    every button works and you cannot break anything that is yours.
  </div>
  <div class="grid" style="grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">
    <div class="box" style="background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:13px">
      <div class="kplab" style="margin-top:0">The author wrote</div>
      <div class="note" style="line-height:1.7">A page of notes: seven scenes with rough times, four creatures
      with numbers, one homebrew rule, a puzzle with its answer, and three things they hadn&rsquo;t decided yet.</div>
    </div>
    <div class="box" style="background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:13px">
      <div class="kplab" style="margin-top:0">Claude filled in</div>
      <div class="note" style="line-height:1.7">The stat block they left blank, the maps they described in one
      line, the key beats for a scene they wrote as prose, and one handout they never mentioned.
      <b style="color:var(--red)">Four things &mdash; and all four are outlined in red.</b></div>
    </div>
  </div>
  <div class="kplab">Try these, in order</div>
  <ol class="note" style="line-height:1.95;padding-left:20px;margin:0">
    <li>Press the red <b>4 to review</b> pill in the header. It walks you to each thing Claude added, one click
      at a time, opening the right tab on the way. Read the note, press <b>&#10003; That&rsquo;s fine</b>, move on.</li>
    <li><b>Story</b> &rarr; open a segment. The bullets are what you read mid-scene. Click a thumbnail under
      <b>Show the table</b> to throw it on the players&rsquo; screen.</li>
    <li>Press <b>Players</b> in the header. A second window opens for your other monitor. Their initiative order
      is hidden until you tick it on.</li>
    <li><b>Encounters</b> &rarr; <b>Load into initiative</b> on the last fight. Watch the start-of-combat pop-up,
      and note that every foe now carries a numbered chip for the dice on your table.</li>
    <li><b>Tools</b> &rarr; roll <span style="font-family:var(--mono)">4d6kh3</span>, work the Damp resolver,
      and open the strongbox handout to see a puzzle with its solution attached.</li>
    <li><b>Story</b> &rarr; <b>&#8681; Story PDF</b> prints the whole adventure as something you can read
      away from the screen.</li>
  </ol>
  <div class="note" style="margin-top:13px;padding-top:11px;border-top:1px solid var(--line)">
    Nothing is locked. Every card has a <b>&#8942;</b> menu, <b>Ctrl+Z</b> undoes anything, and
    <b>Ctrl+K</b> jumps to anything. This panel disappears the moment you load a fight.
  </div>
</div>
"""

boot = ("\n<script>\n/* ---- demonstration content: a short worked oneshot ---- */\n(function(){\n"
        "  const DEMO=" + json.dumps(STATE, ensure_ascii=False) + ";\n"
        "  S=Object.assign(S,JSON.parse(JSON.stringify(DEMO)));\n"
        "  S.party.forEach(p=>{p.id=nid()});\n"
        "  S.clock.last=performance.now();\n"
        "  seedData(); normData(); ensureSceneState();\n"
        "  const n=document.getElementById('notes'); if(n)n.value=S.notes||'';\n"
        "  applyTheme(); paintBrand(); paintAIPill();\n"
        "  renderMon(); renderEnc(); renderTools(); renderScenes(); renderInit(); renderParty();\n"
        "  const wel=document.getElementById('welcome');\n"
        "  if(wel)wel.outerHTML=" + json.dumps(DEMO_PANEL) + ";\n"
        "  const ei=document.getElementById('emptyInit'); if(ei)ei.style.display='none';\n"
        "  undoStack=[]; paintUndo(); savedJSON=snapJSON(); paintSave();\n"
        "})();\n</script>\n")
# NB: PLAYER_DOC inside the app contains its own </body>, so anchor on the real end of file
tail = '</script>\n</body>\n</html>'
assert src.rstrip().endswith('</html>')
i = src.rindex('</body>')
out = src[:i] + boot + src[i:]
out = out.replace('<title>Table Aid — your session, in one tab</title>',
                  "<title>The Miller's Debt — a Table Aid demonstration</title>",1)
out = out.replace('<span class="bname" id="bname">TABLE AID</span>',
                  '<span class="bname" id="bname">THE MILLER&#39;S DEBT</span>',1)
out = out.replace('<span class="bsub" id="bsub">UNTITLED CAMPAIGN</span>',
                  '<span class="bsub" id="bsub">A DEMONSTRATION</span>',1)
io.open(ROOT/'tracker'/'demo.html','w',encoding='utf-8').write(out)
print('demo.html', len(out), 'chars · state', len(json.dumps(STATE)), 'chars')
