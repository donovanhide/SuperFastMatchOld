from collections import defaultdict,deque
from array import array
from operator import itemgetter

def debug(a,b,first,second,limit,counter,length,left,right,matches,results):
    first_string = a[first[0]:first[0]+length]
    second_string = a[second[0]:second[0]+length]
    print"----------------------"
    print "First: %s Second: %s Limit: %s Counter: %s Length: %s Left: %s Right: %s" %(first,second,limit,counter,length,left,right)
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

# @profile
def hash(string,window_size):
    return array('l',(string[i:i+window_size].__hash__() for i in xrange(0,len(string)-window_size+1)))

# @profile
def gen_hash(string,window_size):
    return (string[i:i+window_size].__hash__() for i in xrange(0,len(string)-window_size+1))

# @profile
def match(a,b,window_size=15,use_generator=False):
    if window_size<2:
        raise ValueError
    matches=deque()
    matches_append = matches.append
    results=[]

    if use_generator:
        a_slices = gen_hash(a,window_size)
        b_slices = gen_hash(b,window_size)
        common = set(gen_hash(a,window_size)).intersection(gen_hash(b,window_size))
    else:
        a_slices = hash(a,window_size)
        b_slices = hash(b,window_size)
        common = set(a_slices).intersection(b_slices)
    
    b_dict = defaultdict(deque)
        
    for i,b_slice in enumerate(b_slices):
        if b_slice in common:
            b_dict[b_slice].append(i)

    for i,a_slice in enumerate(a_slices):
        if a_slice in common:
            for b_slice in b_dict[a_slice]:
                matches_append((i,b_slice,))
                
    dump(matches)

    
    while(len(matches)>1):
        first = matches.popleft()
        counter = 0
        length = window_size
        while(counter<len(matches)):
            second = matches[counter]
            limit = length-window_size+1
            left = second[0]-first[0]
            right = second[1]-first[1]
            # debug(a,b,first,second,limit,counter,length,left,right,matches,results)
            if left!=right and left<=limit:
                counter+=1
            elif left>limit:
                break
            else: # left==right
                matches.remove(second)
                length+=1

        results.append((first[0],first[1],length))
        assert(a[first[0]:first[0]+length]==b[first[1]:first[1]+length]),(first,length)
    if len(matches)==1:
        results.append(matches.pop()+(window_size,))
    results.sort(key=itemgetter(0,1))    
    return sorted(results,key=itemgetter(2),reverse=True)

if __name__ == "__main__":
    def getFile(path,url,encoding):
        import os,codecs
        if not os.path.exists(path):
            f = open(path,'w')
            f.write(urllib.urlopen(url).read())
            f.close()
        return codecs.open(path,encoding=encoding).read()

    s1 = getFile('koran.txt','http://www.gutenberg.org/ebooks/2800.txt.utf8','utf-8').split('*END*')[-1]
    s2 = getFile('bible.txt','http://www.gutenberg.org/ebooks/10','utf-8').split('*END*')[-1]
    matches = match(s1,s2,20,True)
