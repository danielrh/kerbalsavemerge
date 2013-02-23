import sys
import json
def lastHash(a,b):
    wherea=a.rfind('#')
    whereb=b.rfind('#')
    return int(a[wherea+1:])-int(b[whereb+1:])
def unHash(a):
    return a[0:a.rfind('#')]
def equivalent(a,b):
    return unHash(a)==unHash(b);
counter=0
def readornUnadornedName(unadornedName):
    global counter
    counter+=1
    return unadornedName+'#'+str(counter)
def readornAdornedName(adornedName):
    return readornUnadornedName(unHash(adornedName))

def copyProperty(dest,source,adornedName):
    global counter;
    counter+=1
    toBeCopied = source[adornedName]
    newKey = readornAdornedName(adornedName)
    if type(toBeCopied)==type(source):
        dest[newKey]=copyAndReturnObject(toBeCopied)
    else:
        dest[newKey]=toBeCopied

def copyAndReturnObject(source):
    retval={}
    for subProperty in getAdornedKeys(source):
        copyProperty(retval,source,subProperty)
    return retval

def getAdornedKeys(obj):
    keySet=[]
    for key in obj:
        keySet+=[key]
    keySet.sort(lastHash);
    return keySet;

def getAdornedTypeKeys(obj,name):
    keySet=[]
    for key in obj:
        if unHash(key)==name:
            keySet+=[key]
    keySet.sort(lastHash);
    return keySet;

def getUnadornedKeys(obj):
    keySet=getAdornedKeys(obj)
    tracking={}
    retval=[]
    for key in keySet:
        unadorned = unHash(key)
        if not (unadorned in tracking):
            tracking[unadorned]=True
            retval+=[unadorned]
    return retval;

def getValues(obj,propName):
    keySet=[]
    for key in obj:
        if equivalent(key,propName):
            keySet+=[key]
    keySet.sort(lastHash)
    retval=[]
    for key in keySet:
        retval+=[obj[key]];
    return retval;
def getSingle(obj,propName):
    retval = getProperties(obj,propName)
    if (len(retval)):
        return retval[0];
    return None;
#takes in 3 objects, the parent node, the first object and the second object return a jsonable object
def mergeObjects (parent,left,right,nodeNameToMerge):
    topLevelDoneSoFar={}
    parentKeys = getAdornedKeys(parent);
    leftKeys = getAdornedKeys(left);
    rightKeys = getAdornedKeys(right);
    retval={}
    print "LEFT KEYS "+str(leftKeys)
    for key in leftKeys:
        uh = unHash(key)
        if uh!=nodeNameToMerge:
            topLevelDoneSoFar[uh]=True
            copyProperty(retval,left,key)
        else:
            break;
    
    for key in rightKeys:
        uh = unHash(key)
        if uh!=nodeNameToMerge:
            if not (uh in topLevelDoneSoFar):
                copyProperty(retval,right,key)
            else:
                pass
        else:
            break;
    mergeXDESCStates(retval,parent,left,right,nodeNameToMerge);
    #now do post-game items
    gameEncountered=False;
    for key in leftKeys:
        uh = unHash(key)
        if uh!=nodeNameToMerge:
            if gameEncountered:
                topLevelDoneSoFar[uh]=True
                copyProperty(retval,left,key)
        else:
            gameEncountered=True
    gameEncountered=False;    
    for key in rightKeys:
        uh = unHash(key)
        if uh!=nodeNameToMerge:
            if gameEncountered:
                if not (uh in topLevelDoneSoFar):
                    copyProperty(retval,right,key)
        else:
            gameEncountered=True
    return retval
def mergeXDESCStates(retval,parent,left,right,XDESC):
    pgame=getAdornedTypeKeys(parent,XDESC);
    lgame=getAdornedTypeKeys(left,XDESC);
    rgame=getAdornedTypeKeys(right,XDESC);
    for index in range(max(len(lgame),len(rgame))):
        if index<len(lgame) and index<len(rgame):
            curKey = readornUnadornedName(XDESC)
            if (index<len(pgame)):
                retval[curKey]=mergeLevelObjects[XDESC](parent[pgame[index]],left[lgame[index]],right[rgame[index]])
            else:
                print("ERROR: merging "+XDESC+" element: count mismatch");
        elif index<len(lgame):
            copyProperty(retval,left,lgame[index])
        elif index<len(rgame):
            copyProperty(retval,right,rgame[index])            
def mergeGameStates(parent,left,right):
    return mergeObjects(parent,left,right,"GAME");
def mergeFlightstateStates(parent,left,right):
    return mergeObjects(parent,left,right,"FLIGHTSTATE");

def mergeTopLevelObjects(parent,left,right):
    return mergeObjects(parent,left,right,"GAME")
def mergeGameLevelObjects(parent,left,right):
    return mergeObjects(parent,left,right,"FLIGHTSTATE")
def mergeCrewVesselLevelObjects(parent,left,right):
    #print "Crew Vessel: "+str(getAdornedKeys(left))
    return {}

mergeLevelObjects={"":mergeGameStates,"GAME":mergeFlightstateStates,"FLIGHTSTATE":mergeCrewVesselLevelObjects}
def merge (parent,left,right):
    return mergeObjects(parent,left,right,"GAME")

def mergeFilesIntoObject (parentfilename, leftfilename, rightfilename):
    return merge(json.loads(open(parentfilename).read()),
                 json.loads(open(leftfilename).read()),
                 json.loads(open(rightfilename).read()));
obj=None
if len(sys.argv)>3:
    obj = mergeFilesIntoObject(sys.argv[3],sys.argv[1],sys.argv[2]);
elif len(sys.argv)>2:
    obj = mergeFilesIntoObject(sys.argv[1],sys.argv[1],sys.argv[2]);    
if obj:
    print json.dumps(obj)
