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
import traceback
import sys
import json

def objectEnd(line):
    if line.strip()=='}':
        return True
    return False
def parseVarName(line):
    where=line.find(" = ");
    if where==-1:
        return line.strip();
    return line[0:where].strip()
def parseVarValue(line):
    where=line.find(" = ");
    if where==-1:
        return None
    return line[where+3:].strip()
def parseVarObject(line):
    if line.strip()=='{':
        return True
    return False
counter=0
def uniqueVarName(var):
    global counter
    counter+=1
    return var+"#"+str(counter)

def readObject (dest,data,offset):
    try:
        while not objectEnd(data[offset]):
            var = parseVarName(data[offset])
            val = parseVarValue(data[offset]);
            printableVar = uniqueVarName(var);
            if (val==None):
                if offset+1>=len(data):
                    return offset#eof
                try:
                    if parseVarObject(data[offset+1]):
                        val = {}
                        offset = readObject(val,data,offset+2);
                    else:
                        print("Parse error on line "+str(offset)+"  var = "+var)
                except:
                    print("ICE "+str(offset)+"  var = "+var)
                    traceback.print_exc(file=sys.stdout)
            else:
                offset+=1;
            dest[printableVar]=val
    except:
        traceback.print_exc(file=sys.stdout)
        raise
    return offset+1

def readSFS(filename):
    f=open(filename);

    data = f.read().decode('utf8').split("\r\n");
    tree = {};
    try:
        readObject(tree,data,0);
    except:
        print ("Error finding closing brace")
    return tree;
if sys.argv and len(sys.argv)>1:
    tree=readSFS(sys.argv[1]);
    outstr=json.dumps(tree,sort_keys=True,indent=4);
    of = open(sys.argv[1].replace(".sfs",".json"),"w");
    of.write(outstr)
    print (tree)
#
