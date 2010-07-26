#!/usr/bin/python
# -*- coding: utf-8 -*-
import superfastmatch

# @profile
def simpletest():
    s1 = "I 'm a test with a section that will be repeated repeated testingly testingly"
    s2 = "I will be repeated repeated testingly 123 testingly"
    matches = superfastmatch.superfastmatch(s1,s2,4)
    for match in matches:
            for submatch in match[4]:
                print '(%s,%s,%s,%s),(%s,%s,%s,%s)"%s","%s"' %( match[0],match[1],match[2],match[3],submatch[0],submatch[1],submatch[2],submatch[3],s1[match[1]:match[2]], s2[submatch[1]:submatch[2]])

# # @profile
def unicodetest():
    s1 = u"From time to time this submerged or latent theater in becomes almost overt. It is close to the surface in Hamlet’s pretense of madness, the “antic disposition” he puts on to protect himself and prevent his antagonists from plucking out the heart of his mystery. It is even closer to the surface when Hamlet enters his mother’s room and holds up, side by side, the pictures of the two kings, Old Hamlet and Claudius, and proceeds to describe for her the true nature of the choice she has made, presenting truth by means of a show. Similarly, when he leaps into the open grave at Ophelia’s funeral, ranting in high heroic terms, he is acting out for Laertes, and perhaps for himself as well, the folly of excessive, melodramatic expressions of grief."
    s2 = u"Almost all of Shakespeare’s Hamlet can be understood as a play about acting and the theater. For example, there is Hamlet’s pretense of madness, the “antic disposition” that he puts on to protect himself and prevent his antagonists from plucking out the heart of his mystery. When Hamlet enters his mother’s room, he holds up, side by side, the pictures of the two kings, Old Hamlet and Claudius, and proceeds to describe for her the true nature of the choice she has made, presenting truth by means of a show. Similarly, when he leaps into the open grave at Ophelia’s funeral, ranting in high heroic terms, he is acting out for Laertes, and perhaps for himself as well, the folly of excessive, melodramatic expressions of grief."
    matches = superfastmatch.superfastmatch(s1,s2,4)
    for match in matches:
          for submatch in match[4]:
              print '(%s,%s,%s),(%s,%s,%s)"%s","%s"' %( match[1],match[2],match[3],submatch[1],submatch[2],submatch[3],s1[match[1]:match[2]].encode('utf-8'), s2[submatch[1]:submatch[2]].encode('utf-8'))

def nonunicodetest():
    s1 = u"From time to time this submerged or latent theater in becomes almost overt. It is close to the surface in Hamlet’s pretense of madness, the “antic disposition” he puts on to protect himself and prevent his antagonists from plucking out the heart of his mystery. It is even closer to the surface when Hamlet enters his mother’s room and holds up, side by side, the pictures of the two kings, Old Hamlet and Claudius, and proceeds to describe for her the true nature of the choice she has made, presenting truth by means of a show. Similarly, when he leaps into the open grave at Ophelia’s funeral, ranting in high heroic terms, he is acting out for Laertes, and perhaps for himself as well, the folly of excessive, melodramatic expressions of grief."
    s2 = u"Almost all of Shakespeare’s Hamlet can be understood as a play about acting and the theater. For example, there is Hamlet’s pretense of madness, the “antic disposition” that he puts on to protect himself and prevent his antagonists from plucking out the heart of his mystery. When Hamlet enters his mother’s room, he holds up, side by side, the pictures of the two kings, Old Hamlet and Claudius, and proceeds to describe for her the true nature of the choice she has made, presenting truth by means of a show. Similarly, when he leaps into the open grave at Ophelia’s funeral, ranting in high heroic terms, he is acting out for Laertes, and perhaps for himself as well, the folly of excessive, melodramatic expressions of grief."
    matches = superfastmatch.superfastmatch(s1,s2,8)
    for match in matches:
        for submatch in match[4]:
            print '(%s,%s,%s),(%s,%s,%s)"%s","%s"' %( match[1],match[2],match[3],submatch[1],submatch[2],submatch[3],s1[match[1]:match[2]].encode('utf-8'), s2[submatch[1]:submatch[2]].encode('utf-8'))


if __name__ == "__main__":
    simpletest()
    # unicodetest()
    # nonunicodetest()