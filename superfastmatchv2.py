#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict,deque
from operator import itemgetter
import codecs,urllib

# @profile
def slices(string,window_size):
    return [string[i:i+window_size] for i in xrange(0,len(string)-window_size)]

# @profile
def match(a,b,window_size=15):
    matches=deque()
    results=[]
    a_slices = slices(a,window_size)
    b_slices = slices(b,window_size)
    b_dict = defaultdict(list)
    common = set(a_slices) & set(b_slices)
    
    for i,b_slice in enumerate(b_slices):
        if b_slice in common:
            b_dict[b_slice].append((i,window_size))

    for i,a_slice in enumerate(a_slices):
        if a_slice in common:
            matches.appendleft((i,window_size,b_dict[a_slice]))
            
    while(len(matches)>1):
        first = matches.pop()
        if (matches[-1][0]-first[0])<first[1]:
            second = matches.pop()
            submatches = [(submatch[0],submatch[1]+1) for submatch in first[2]]
            combined = (first[0],first[1]+1,submatches)
            # print first,second,combined #Beautiful!
            matches.append(combined)
        else:    
            results.append(first)
    if len(matches)==1:
        results.append(matches.pop())
    return sorted(results,key=itemgetter(1),reverse=True)

def printresults(matches,s1,s2):
    for match in matches:
        for submatch in match[2]:
            print '(%s,%s),(%s,%s)"%s","%s"' %( match[0],match[1],submatch[0],submatch[1],s1[match[0]:match[0]+match[1]].encode('utf-8'), s2[submatch[0]:submatch[0]+submatch[1]].encode('utf-8'))

bible = urllib.urlopen('http://www.gutenberg.org/cache/epub/10/pg10.txt').read()
s1 = bible[:len(bible)/2]
s2 = bible[len(bible)/2:]
matches = match(s1,s2,15)
printresults(matches[:40],s1,s2)
print len(matches)


# s1 = codecs.open('long.txt',encoding='utf-8').read()
# s2 = u"""The Secretary of State for Culture, Media and Sport, The Rt Hon James Purnell MP, announced today a capital investment of £50 million towards the new development of Tate Modern. This is the largest capital commitment by Government to a cultural project since the British Library which opened in 1998. Nicholas Serota, Director Tate, said: “Today’s announcement is an important endorsement by Government of the contribution that the arts make to society as a whole and the importance of British art at an international level. It gives us a platform for the creation of an institution for the 21st century, designed to serve the next generation of artists and visitors. This commitment confirms London’s position as one of the leading international centres for the visual arts.” The Success of Tate Modern In 2000, an investment of £137 million of public and private money created Tate Modern. In just seven years, the gallery has become most popular museum of modern art in the world. It has attracted over 30 million visitors since it opened and is Britain’s second leading tourist attraction. Around 60% of visitors are under 35 years of age. The gallery has helped revive a wide area of inner London, helping to reconfigure cultural tourism along the South Bank, creating up to 4,000 new jobs. The Need to Develop Tate Modern In spite of its success, much of Tate Modern’s potential is still to be realised. One third of the building remains derelict and needs to be brought into use. The building was originally designed for 1.8 million visitors a year. With present audiences at nearly 5 million, there is serious overcrowding in the galleries, particularly at weekends, and there is an urgent need to improve and extend facilities. Different kinds of galleries are required to show art forms new to Tate, including photography, video, film and performance, as well as more galleries to show major exhibitions in their entirety. Bigger spaces are needed to meet the requirements of Tate’s growing number of large-scale works and installations. With additional space, more of Tate’s Collection can go on view and key paintings, sculptures and installations can be brought out of storage and displayed on a more permanent basis. The New Building The new development, by internationally celebrated architects, Herzog & de Meuron, will create a spectacular new building adjoining Tate Modern to the south, on the foundation of the former power station’s oil tanks. This will be Britain’s most important new building for culture since the creation of the Royal National Theatre in 1976, the Barbican in 1982, and the British Library in 1998. The new building will increase Tate Modern’s size by 60% adding approximately 21,000 square metres of new space. The development will provide more space for contemporary art and enable Tate to explore new areas of contemporary visual culture involving photography, film, video and performance, enriching its current programme. Tate Modern’s outstanding and pioneering education programme will at last have the space to meet its potential and serve a new and broader audience. New Cultural Quarter The new development of Tate Modern will create a dynamic new part of London – a creative campus stretching southwards. A new entrance on the south side will open up a north-south route or ‘street’ right through the building, creating a pedestrian way from the City across the MillenniumBridge through the Turbine Hall to Southwark and the Elephant and Castle. The new development lies at the heart of London’s cultural quarter running from the London Eye to the DesignMuseum and consisting of a group of more than 20 cultural organisations. Next Steps The designs for the new building were granted planning permission by Southwark Council in March 2007 with the Planning Committee unanimous in its support for the scheme. The project will now enter its detailed design phase and a project team is being appointed. The total costs of the project are comparable to the costs of creating the original Tate Modern: £165 million in 2006 prices, £215 million at outturn in 2012. A projected additional 1 million visitors a year will increase Tate Modern’s operating revenues significantly. The Mayor of London has given a major investment of £7 million from the LDA towards the development and help fast-track the scheme so that it might be completed in time for the Olympic Games in 2012. Fundraising from the private sector is progressing well and includes the recent"""
# matches = match(s1,s2,15)
# printresults(matches,s1,s2)
# print len(matches)