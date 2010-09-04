#!/usr/bin/python
# -*- coding: utf-8 -*-
import superfastmatch
import unittest 

def printresults(matches,s1,s2):
    nums=""
    for a in range(0,max(len(s1),len(s2))):
        nums+= str(a)[-1]
    print nums
    print s1.encode('utf-8')
    print s2.encode('utf-8')
    for match in matches:
          for submatch in match[4]:
              print '(%s,%s,%s,%s),(%s,%s,%s,%s)"%s","%s"' %( match[0],match[1],match[2],match[3],submatch[0],submatch[1],submatch[2],submatch[3],s1[match[1]:match[2]+1].encode('utf-8'), s2[submatch[1]:submatch[2]+1].encode('utf-8'))

class TestSuperFastMatch(unittest.TestCase):
    def test_equal(self):
        s1 = "1234"
        s2 = "1234"
        matches = superfastmatch.superfastmatch(s1,s2,1)
        self.assertEqual(len(matches),1)
        printresults(matches,s1,s2)
    
    def test_singleword(self):
        s1 = "fantastic"
        s2 = "fantastic123"
        matches = superfastmatch.superfastmatch(s1,s2,1)
        self.assertEqual(len(matches),1)
        printresults(matches,s1,s2)
    
    def test_ending(self):
        s1 = "fantastic blank 12345"
        s2 = "fantastic12345"
        matches = superfastmatch.superfastmatch(s1,s2,1)
        self.assertEqual(len(matches),3)
        printresults(matches,s1,s2)
    
    def test_simple(self):
        s1 = "I'm a test with a section that will be repeated repeated testingly testingly"
        s2 = "I will be repeated repeated testingly 123 testingly"
        matches = superfastmatch.superfastmatch(s1,s2,6)
        self.assertEqual(len(matches),2)
        printresults(matches,s1,s2)
    
    def test_short_unicode(self):
        s1 = u"This is “unicode”"
        s2 = u"unicode I am"
        matches = superfastmatch.superfastmatch(s1.encode('latin-1','replace'),s2.encode('latin-1','replace'),2)
        printresults(matches,s1,s2)
    
    def test_unicode(self):
        s1 = u"From time to time this submerged or latent theater in becomes almost overt. It is close to the surface in Hamlet’s pretense of madness, the “antic disposition” he puts on to protect himself and prevent his antagonists from plucking out the heart of his mystery. It is even closer to the surface when Hamlet enters his mother’s room and holds up, side by side, the pictures of the two kings, Old Hamlet and Claudius, and proceeds to describe for her the true nature of the choice she has made, presenting truth by means of a show. Similarly, when he leaps into the open grave at Ophelia’s funeral, ranting in high heroic terms, he is acting out for Laertes, and perhaps for himself as well, the folly of excessive, melodramatic expressions of grief."
        s2 = u"Almost all of Shakespeare’s Hamlet can be understood as a play about acting and the theater. For example, there is Hamlet’s pretense of madness, the “antic disposition” that he puts on to protect himself and prevent his antagonists from plucking out the heart of his mystery. When Hamlet enters his mother’s room, he holds up, side by side, the pictures of the two kings, Old Hamlet and Claudius, and proceeds to describe for her the true nature of the choice she has made, presenting truth by means of a show. Similarly, when he leaps into the open grave at Ophelia’s funeral, ranting in high heroic terms, he is acting out for Laertes, and perhaps for himself as well, the folly of excessive, melodramatic expressions of grief."
        matches = superfastmatch.superfastmatch(s1.lower().encode('latin-1','replace'),s2.lower().encode('latin-1','replace'),8)
        printresults(matches,s1,s2)
        self.assertEqual(len(matches),5)
        
    def test_bug_from_site(self):
        s1=u'\nThe body of a man has been recovered from the River Tweed near Coldstream following a police operation.\nIt follows an eight-day river search for missing man Philip Shoemaker, 51, from Kelso by Lothian and Borders Police.\nRescue units and a helicopter joined search teams in the area following several reports received from members of the public.\nNo formal identification has been made of the man found in the river.\n'
        s2=u'\nAt 12.26pm on Monday, April 23, reports were received of a body lying on the mud flats between the Redheugh Bridge and King Edward Bridge over the River Tyne.\nNorthumbria Police Marine Unit attended and discovered the body of an elderly man.\nThe body was recovered but has not yet been formally identified.\xa0 There are no suspicious circumstances regarding this incident.'
        matches = superfastmatch.superfastmatch(s1.lower().encode('latin-1','replace'),s2.lower().encode('latin-1','replace'),15)
        print matches
        printresults(matches,s1,s2)
        self.assertEqual(len(matches),0)
    
    def test_long_one(self):
        s1=u"""at 12.40am on Sunday, August 5, police were called to the Cashmere nightclub in Berwick after the CCTV operator at Berwick police station saw that signs of a dispute between two factions who had been refused admission to the club by the doorstaff. A total of four officers were called to respond. When the first two arrived at the scene both factions turned on them and assaulted them. One officer was punched to the ground and continued to be attacked as he lay unconscious. The second officer received face and body injuries. By this time two more officers arrived at the scene and were also assaulted. More resources were called out, including officers from Alnwick, the area support group from Hexham, dog handlers and the North East Air Support Unit. Officers from Lothian and Borders police also gave assistance at the scene. The doorstaff also gave valuable assistance to bring the situation under control. Four men were arrested. The four, aged 18, 33, 34 and 44, are all from Berwick and were arrested on suspicion of causing grievous bodily harm, violent disorder and drunk and disorderly. The first four officers on the scene, who are all male,  work at Northumberland area command and are based in Berwick. They were all wearing regulation body armour. Their ages range from 30 to 42.  The officers  who were taken to hospital, one aged 39 and one aged 42, continue to be detained. Both are experienced officers with Northumbria, one with 11 years' service and the other 17. Their injuries are not considered life threatening and both are in a stable condition. A total of four other officers - three men and a woman -  will receive medical attention from the force's Occupational Health Unit. Supt Gordon Milward, Northumberland area command, said: "First of all I must stress that this incident was totally out of character for Berwick, where disorder like this is extremely uncommon. We still don't know why what started as a dispute outside a club should have escalated in this way. "Attacks against police officers are totally unacceptable and there is no doubt that without the assistance of the doorstaff the outcome could have been even more serious. Fortunately, the officers' injuries do not appear to be as serious as was first thought, but any attack against a police officer is one too many. "We are leaving no stone unturned in the investigation to bring those responsible to justice. We are carrying out an extensive review of all CCTV coverage in the town centre overnight in an effort to trace anyone acting suspiciously in and around the Golden Square area. It's highly likely that more arrests will be made. We are also increasing reassurance patrols around Berwick." Anyone with information is asked to contact Northumbria Police on 08456 043 043 or call Crimestoppers."""
        s2=u"""Two police officers are in hospital after they were attacked outside a Northumberland nightclub. One of the men, who had been called to a dispute at the Cashmere club in Berwick, was punched to the ground and attacked again as he lay unconscious. The second officer suffered facial and body injuries in the clash, believed to have been sparked when two groups of people were refused admission. Four Berwick men, aged 18 to 44, have been arrested. They are being questioned over the incident, which happened in the early hours of Sunday. The two officers were taken to Wansbeck General Hospital, where their condition is described as stable. Police said the disturbance broke out after two separate groups of revellers were refused admission to the nightclub. Four police officers were called to the scene by CCTV operators and the two groups joined force to attack the officers when they arrived. Reinforcements were called out from Alnwick, and four other police officers were hurt in the clashes. The club's door staff have been praised for helping to bring the incident under control. 'More arrests' Supt Gordon Milward, of Northumbria Police, said: "We still don't know why what started as a dispute outside a club should have escalated in this way. "Attacks against police officers are totally unacceptable and there is no doubt that without the assistance of the door staff the outcome could have been even more serious. "We are leaving no stone unturned in the investigation to bring those responsible to justice. "It's highly likely that more arrests will be made." Officers are now reviewing CCTV coverage in the town centre as part of the investigation."""
        matches = superfastmatch.superfastmatch(s1.lower().encode('latin-1','replace'),s2.lower().encode('latin-1','replace'),15)
        printresults(matches,s1,s2)
        self.assertEqual(len(matches),21)
    
    def test_hashes(self):
        s = "I need to be hashed"
        hashes = superfastmatch.hashes(s,15)
        print hashes
        self.assertEqual(len(hashes),5)
        
    def test_hashwindow(self):
        s = "hash"
        hashes = superfastmatch.hashes(s,2)
        for i in range(0,len(hashes)):
            print s[i:i+2],hashes[i]
        self.assertEqual(len(hashes),3)
        
if __name__ == "__main__":
    unittest.main()
