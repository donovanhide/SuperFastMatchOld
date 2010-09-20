from collections import defaultdict,deque
from operator import itemgetter

def debug(a,b,first,second,limit,counter,left_offset,right_offset,matches,results):
    first_string = a[first[0]:first[0]+first[2]]
    second_string = a[second[0]:second[0]+second[2]]
    print"----------------------"
    print "First: %s Second: %s Limit: %s Counter: %s Left Offset: %s Right Offset: %s" %(first,second,limit,counter,left_offset,right_offset)
    print first_string.encode('utf-8'),'|',second_string.encode('utf-8')
    print"----------------------"
    for match in list(matches)[:10]:
        print match
    print"----------------------"
    for result in results:
        print result
    print"----------------------"
    raw_input()

def dump(matches):
    for match in matches:
        print match
    raw_input()

def text(string,window_size):
    return [string[i:i+window_size] for i in xrange(0,len(string)-window_size+1)]

def match(a,b,window_size=15,func=text):
    if window_size<2:
        raise ValueError
    matches=deque()
    results=[]

    a_slices = func(a,window_size)
    b_slices = func(b,window_size)
    b_dict = defaultdict(list)
    common = set(a_slices) & set(b_slices)

    for i,b_slice in enumerate(b_slices):
        if b_slice in common:
            b_dict[b_slice].append(i)

    for i,a_slice in enumerate(a_slices):
        if a_slice in common:
            for b_slice in b_dict[a_slice]:
                matches.append((i,b_slice,window_size,))

    # dump(sorted(list(matches),key=itemgetter(0,1)))
    # dump(matches)
    
    while(len(matches)>1):
        first = matches.popleft()
        counter = 0
        while(counter<len(matches)):
            second = matches[counter]
            limit = first[2]-window_size+1
            left_offset = second[0]-first[0]
            right_offset = second[1]-first[1]
            # debug(a,b,first,second,limit,counter,left_offset,right_offset,matches,results)
            if left_offset==right_offset:    
                matches.remove(second)
                first = (first[0],first[1],first[2]+1)
                # assert(a[first[0]:first[0]+first[2]]==b[first[1]:first[1]+first[2]]), (a[first[0]:first[0]+first[2]],b[first[1]:first[1]+first[2]])
            elif left_offset>limit:
                      break
            else:
                counter+=1
        results.append(first)
    if len(matches)==1:
        results.append(matches.pop())
    results.sort(key=itemgetter(0,1))    
    return sorted(results,key=itemgetter(2),reverse=True)