#/*********************************************
# * CopyrigCopyright (c) 2012, The Tree House
# *
# * All rights reserved.
# *
# * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# *
# * - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ************************************************/
import sys
import json
def newline(tablevel):
    s="\r\n";
    for i in range(tablevel):
        s+="\t";
    return s;
def lastHash(a,b):
    wherea=a.rfind('#')
    whereb=b.rfind('#')
    return int(a[wherea+1:])-int(b[whereb+1:])
def unHash(a):
    return a[0:a.rfind('#')]
def dumpObject(obj,tablevel):
    retval=""
    keyList=[]
    for key in obj:
        keyList+=[key]
    keyList.sort(lastHash)
    for k in keyList:
        retval+=newline(tablevel)+unHash(k)
        if type(obj[k])==type(obj):#if it's another object
            retval+=newline(tablevel)+'{'
            retval+=dumpObject(obj[k],tablevel+1)
            retval+=newline(tablevel)+'}'
        else:
            retval+=" = ";
            retval+=obj[k]
    return retval
def readSFS(filename):
    data = open(filename).read();
    tree=json.loads(data)
    return dumpObject(tree,0)[len(newline(0)):]+"\r\n";#need that trailing newline
    
if sys.argv and len(sys.argv)>1:
    data=readSFS(sys.argv[1]);
    of = open(sys.argv[2],"w");
    of.write(data)
    print (data)
#
