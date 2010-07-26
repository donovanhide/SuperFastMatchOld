#include "stdint.h" /* Replace with <stdint.h> if appropriate */
#include "Python.h"
#include "string.h"

/* note that this is completely and totally lifted from Paul Hsieh:
http://www.azillionmonkeys.com/qed/hash.html */

#undef get16bits
#if (defined(__GNUC__) && defined(__i386__)) || defined(__WATCOMC__) \
  || defined(_MSC_VER) || defined (__BORLANDC__) || defined (__TURBOC__)
#define get16bits(d) (*((const uint16_t *) (d)))
#endif

#if !defined (get16bits)
#define get16bits(d) ((((uint32_t)(((const uint8_t *)(d))[1])) << 8)\
                       +(uint32_t)(((const uint8_t *)(d))[0]) )
#endif

/* this is hocked from the superfasthash implementation
http://www.azillionmonkeys.com/qed/hash.html
*/
uint32_t SuperFastHash (const char * data, int len) {
uint32_t hash = len, tmp;
int rem;

    if (len <= 0 || data == NULL) return 0;

    rem = len & 3;
    len >>= 2;

    /* Main loop */
    for (;len > 0; len--) {
        hash  += get16bits (data);
        tmp    = (get16bits (data+2) << 11) ^ hash;
        hash   = (hash << 16) ^ tmp;
        data  += 2*sizeof (uint16_t);
        hash  += hash >> 11;
    }

    /* Handle end cases */
    switch (rem) {
        case 3: hash += get16bits (data);
                hash ^= hash << 16;
                hash ^= data[sizeof (uint16_t)] << 18;
                hash += hash >> 11;
                break;
        case 2: hash += get16bits (data);
                hash ^= hash << 11;
                hash += hash >> 17;
                break;
        case 1: hash += *data;
                hash ^= hash << 10;
                hash += hash >> 1;
    }

    /* Force "avalanching" of final 127 bits */
    hash ^= hash << 3;
    hash += hash >> 5;
    hash ^= hash << 4;
    hash += hash >> 17;
    hash ^= hash << 25;
    hash += hash >> 6;

    return hash;
}


PyObject * GetHashes(const char * data, int len, int windowsize){
    int numhashes = len - windowsize;
	if (windowsize >= len) {
		numhashes = 1;
		windowsize = len;
	}
    PyObject* list = PyList_New(numhashes);
	int i;
	for (i = 0; i < numhashes; i++) {   
        PyList_SetItem(list,i,PyInt_FromLong(SuperFastHash(data + i, windowsize))); 
	}
    return list;
}


static PyObject * superfastmatch (PyObject *self, PyObject *args) {
	const char *a_data;
    const char *b_data;
	int a_len, b_len, windowsize;
	
	PyArg_ParseTuple(args, "s#s#i", &a_data, &a_len, &b_data, &b_len, &windowsize); 
    PyObject* unfiltered = PyList_New(0);
    PyObject* filtered = PyList_New(0);

    int counter;
    do{
        counter = 0;
        PyObject* a_list = GetHashes(a_data,a_len,windowsize);
        PyObject* a_set = PySet_New(a_list);
        PyObject* b_list = GetHashes(b_data,b_len,windowsize);
        PyObject* b_dict = PyDict_New();

        //Build a dictionary of hashes from b for every hash present in a and initialise a list
        int i;
        for (i=0;i<PySet_Size(a_set);i++){
            PyObject* item = PySet_Pop(a_set);
            PyDict_SetItem(b_dict,item,PyList_New(0));
        }

        //For each hash in dictionary add details from b to a list
        for (i=0;i<PyList_Size(b_list);i++){
            PyObject* hash = PyList_GetItem(b_list,i);
            PyObject* item = PyDict_GetItem(b_dict,hash);
            if (item){
                PyList_Append(item,PyTuple_Pack(4,hash,PyInt_FromLong(i),PyInt_FromLong(i+windowsize),PyInt_FromLong(windowsize)));
            }
        }

        //For each detail in a, if a hash in b exists, connect details
        for (i=0;i<PyList_Size(a_list);i++){
            PyObject* item = PyList_GetItem(a_list,i);
            PyObject* matches = PyDict_GetItem(b_dict,item);
            if (matches && PyList_Size(matches)>0){
                PyObject* tuple = PyTuple_Pack(5,item,PyInt_FromLong(i),PyInt_FromLong(i+windowsize),PyInt_FromLong(windowsize),matches);
                PyList_Append(unfiltered,tuple);  
                counter ++; 
            }
        }   
        
        //Carry on increasing the window until no more found
        windowsize++;
    }while(counter!=0);
    
    
    //Now filter so that only longest substrings remain
    int i,j;
    int overlapping;
    int unfiltered_length = PyList_Size(unfiltered);
    PyList_Append(filtered,PyList_GetItem(unfiltered,unfiltered_length-1));
    //Iterate backwards, ensuring longest matches first
    for (i=(unfiltered_length-2);i>=0;i--){
        overlapping = 0;
        PyObject* candidate = PyList_GetItem(unfiltered,i);
        for (j=0;j<PyList_Size(filtered);j++){
          PyObject* existing = PyList_GetItem(filtered,j);
          if   (((PyInt_AsLong(PyTuple_GetItem(candidate,1)) <= PyInt_AsLong(PyTuple_GetItem(existing,2)))&&
               (PyInt_AsLong(PyTuple_GetItem(candidate,1)) >= PyInt_AsLong(PyTuple_GetItem(existing,1))))
               ||
               (((PyInt_AsLong(PyTuple_GetItem(candidate,2)) <= PyInt_AsLong(PyTuple_GetItem(existing,2)))&&
               (PyInt_AsLong(PyTuple_GetItem(candidate,2)) >= PyInt_AsLong(PyTuple_GetItem(existing,1)))))){
                   overlapping = 1;
          }
        }
        if (overlapping==0){
            PyList_Append(filtered,candidate);
        }
    }
    return filtered;
}


PyMethodDef methods[] = {
    {"superfastmatch", superfastmatch, METH_VARARGS, "Given two strings and a minimum window size, returns the longest substrings which occur in both strings"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC 
initsuperfastmatch()
{
    (void) Py_InitModule("superfastmatch", methods);   
}



