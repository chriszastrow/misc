var mgmt = {
botPerformRole: function(){
    //Define each 'bot' and direct toward role function:
    for(let key in Game.bots){
        let bot = Game.bots[key];
        mod.bot[bot.memory.role](bot)
    }
},
activebotCount: function(){
    //Removes expired bots & updates bot role counters:
    for(let role in mod.bot.botQuota){
        M.C[role] = 0
    }
    for(let key in Memory.bots){
        if(!Game.bots[key]){
            delete Memory.bots[key]
        }
        else{let role = Memory.bots[key].role;
            M.C[role] += 1
        }
    }
},
repairManager: function(){
    //Make lists of structures below hit thresholds:
    M.L.repairRoad = mod.mgmt.listFix(M.S.road,M.V.minHitsRoad);
    M.L.repairContainer = mod.mgmt.listFix(M.S.container,M.V.minHitsContainer);
    //This array defines the repair priority of structure type lists.
    M.L.constructionPriorityList = [M.L.repairContainer,M.L.repairRoad];
    //Iterate damaged structure lists by priority, determine priority target:
    for(let i=0;i<M.L.constructionPriorityList.length;i++){
        for(let x=0;x<M.L.constructionPriorityList[i].length;x++){
            if(M.L.constructionPriorityList[i][x] != null){
                Memory.r0.repairTarget = M.L.constructionPriorityList[i][x].id;
                return true
            }
        }
    }
},
findClosestToMe: function(bot,listName){
    //bot requests to find closest array element to it amongst input array list:
    if(listName != undefined){
        for(let i=0;i<listName.length;i++){
            listName[i].range = bot.pos.getRangeTo(listName[i])
        }
        listName.sort(function(a,b){
            return a.range - b.range
        });
        return listName
    }
},
listFix: function(inputList,hitLimit){//Remove nulls & sort by lowest Hits:
    if(typeof hitLimit === 'undefined'){
        hitLimit = 100000001
    }
    let tempList = [];
    for(i=0;i<inputList.length;i++){
        if(inputList[i] != null && inputList[i].hits < hitLimit){
            tempList.push(inputList[i])
        }
    }
    result = tempList.sort(function(a,b){
        return a.hits - b.hits
    });
	return result;
},
listExtension: function(bot){
    M.L.emptyExtention =  Game.flags['Flag1'].room.find(FIND_STRUCTURES,{
        filter: (e) => { 
        return (e.hits > 0 && e.energy != e.energyCapacity 
        && e.structureType == STRUCTURE_EXTENSION)
        }
    });
},
buildSitePriority: function(){//Filter construction sites, establish #1 priority:
    let priorityConstruction = JSON.parse(RawMemory.segments[0]);
    let tempList = Game.flags['Flag1'].room.find(FIND_MY_CONSTRUCTION_SITES);
    let i = 0;
    prioritize();
    function prioritize(){//recursive list filtering:
        let makeList = tempList.filter(function(element){
            return element.structureType == priorityConstruction[i]
        });
        if(makeList.length > 0){M.L.buildPriority = makeList}
        if(makeList.length == 0 && (i <= priorityConstruction.length)){
            i += 1;
            prioritize()
        }
    }
},
findDroppedEnergy: function(){
    Memory.r0.droppedEnergy = Game.flags['Flag1'].room.lookForAtArea(
        RESOURCE_ENERGY,20,30,48,48,{asArray:true}).filter(function(element,index,array){
        return(element.energy.amount > 50)
    });
},
}
module.exports = mgmt
