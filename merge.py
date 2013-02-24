import sys
import json
def lastHash(a,b):
    wherea=a.rfind('#')
    whereb=b.rfind('#')
    return int(a[wherea+1:])-int(b[whereb+1:])
def unHash(a):
    where=a.rfind('#')
    return a[0:where]
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
    retval = getValues(obj,propName)
    if (len(retval)):
        return retval[0];
    return None;

def copyKeysBeforeMidOrAfter(retval,parent,left,right,nodeNameToMerge,nodeSecondNameToMerge,targetThird):
    leftKeys = getAdornedKeys(left);
    rightKeys = getAdornedKeys(right);
    hitcount=0;
    for key in leftKeys:
        if unHash(key)==nodeNameToMerge or unHash(key)==nodeSecondNameToMerge:
            hitcount+=1
        else:
            if hitcount==targetThird:
                copyProperty(retval,left,key)
    hitcount=0;
    for key in rightKeys:
        if unHash(key)==nodeNameToMerge or unHash(key)==nodeSecondNameToMerge:
            hitcount+=1
        else:
            if hitcount==targetThird and len(getValues(left,key))==0:#of we're in the target third and left doesn't have this key
                copyProperty(retval,right,key)

    

#takes in 3 objects, the parent node, the first object and the second object return a jsonable object
def mergeObjects (parent,left,right,nodeNameToMerge,nodeSecondNameToMerge=None):
    topLevelDoneSoFar={}
    retval={}
    copyKeysBeforeMidOrAfter(retval,parent,left,right,nodeNameToMerge,nodeSecondNameToMerge,0);

    mergeXDESCStates[nodeNameToMerge](retval,parent,left,right,nodeNameToMerge);

    copyKeysBeforeMidOrAfter(retval,parent,left,right,nodeNameToMerge,nodeSecondNameToMerge,1);
    if nodeSecondNameToMerge:
        mergeXDESCStates[nodeSecondNameToMerge](retval,parent,left,right,nodeSecondNameToMerge);
        copyKeysBeforeMidOrAfter(retval,parent,left,right,nodeNameToMerge,nodeSecondNameToMerge,2);

    return retval
def genericMergeKey(retval,parent,left,right,XDESC):
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
def mergeCrew(retval,parent,left,right,crewString):
    pass
def mergeVessel(retval,parent,left,right,vesselString):
    pass
mergeXDESCStates={"GAME":genericMergeKey,"FLIGHTSTATE":genericMergeKey,"CREW":mergeCrew,"VESSEL":mergeVessel}



############the following functions tell
def mergeGameStates(parent,left,right):
    return mergeObjects(parent,left,right,"GAME");
def mergeFlightstateStates(parent,left,right):
    return mergeObjects(parent,left,right,"FLIGHTSTATE");

def mergeCrewVesselLevelObjects(parent,left,right):
    return mergeObjects(parent,left,right,"CREW","VESSEL")

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
