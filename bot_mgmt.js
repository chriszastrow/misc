var mgmt = {
creepPerformRole: function(){//Define each 'creep' and direct it to its role function:
    for(let key in Game.creeps){
        let creep = Game.creeps[key];
        mgmt.goToHome(creep);
        mod.creep[creep.memory.role](creep);//Role filter to class logic, where action & target are assigned.
        //Proceed to do primary action on assigned target, or move toward it:
        if(creep[creep.memory.action](Game.getObjectById(creep.memory.target),RESOURCE_ENERGY) == ERR_NOT_IN_RANGE){
            console.log('ERROR: ' + creep + creep[creep.memory.action](Game.getObjectById(creep.memory.target))); //error reporting.
            creep.moveTo(Game.getObjectById(creep.memory.target),{visualizePathStyle:{
                fill:'transparent',stroke:'#00f',lineStyle:'dashed',strokeWidth:0.1,opacity:0.8}})}}
},
goToHome: function(creep){//Send creep to home location if it has one:
    if(creep.memory.home != undefined && (Game.getObjectById(creep.memory.home).pos.x != creep.pos.x 
        || Game.getObjectById(creep.memory.home).pos.y != creep.pos.y)){
        creep.moveTo(Game.getObjectById(creep.memory.home).pos,{visualizePathStyle:{
            fill:'transparent',stroke:'#00f',lineStyle:'dashed',strokeWidth:0.1,opacity:0.8}})}
},
activeCreepCount: function(){//Removes expired creeps & updates creep role counters:
    for(let role in mod.creep.creepQuota){M.C[role] = 0}
    for(let key in Memory.creeps){
        if(!Game.creeps[key]){delete Memory.creeps[key]}
        else{let role = Memory.creeps[key].role;M.C[role] += 1}}
},
creepSpawner: function(){
    if(M.S.spawn[0] != null){
        if(!M.S.spawn[0].spawning && M.S.spawn[0].room.energyAvailable > 99){
            for(var role in mod.creep.creepQuota){
                if(M.C[role] < mod.creep.creepQuota[role]){
                    mod.creep.creepDictionary[role]()}}}}
},
repairManager: function(){
    //Iterate damaged structure lists by priority, determine priority target:
    for(let i=0;i<M.L.constructionPriorityList.length;i++){
        for(let x=0;x<M.L.constructionPriorityList[i].length;x++){
            if(M.L.constructionPriorityList[i][x] != null){
                //DO NOT REMOVE repairTarget from Memory.r0, it will break towers:
                Memory.r0.repairTarget = M.L.constructionPriorityList[i][x].id;
                console.log(M.L.constructionPriorityList[i][x]);
                return true}}}
},
findClosestToMe: function(creep,listName){
    //creep requests to find closest array element to it amongst input array list:
    if(listName != undefined){
        for(let i=0;i<listName.length;i++){
            listName[i].range = creep.pos.getRangeTo(listName[i])}
        listName.sort(function(a,b){return a.range - b.range});
        return listName}
},
listFix: function(inputList,hitLimit){//Remove nulls & sort by lowest Hits:
    if(typeof hitLimit === 'undefined'){hitLimit = 100000001}
    let tempList = [];
    for(i=0;i<inputList.length;i++){
        if(inputList[i] != null && inputList[i].hits < hitLimit){
            tempList.push(inputList[i])}}
    result = tempList.sort(function(a,b){return a.hits - b.hits});
	return result;
},
listExtension: function(creep){
    M.L.emptyExtention =  Game.flags['Flag1'].room.find(FIND_STRUCTURES,{
        filter: (e) => {
        return (e.hits > 0 && e.energy != e.energyCapacity 
        && e.structureType == STRUCTURE_EXTENSION)}});
},
buildSitePriority: function(){//Filter construction sites, establish #1 priority:
    let priorityConstruction = JSON.parse(RawMemory.segments[0]);
    let tempList = Game.flags['Flag1'].room.find(FIND_MY_CONSTRUCTION_SITES);
    let i = 0;
    prioritize();
    function prioritize(){//recursive list filtering:
        let makeList = tempList.filter(function(element){
            return element.structureType == priorityConstruction[i]});
        if(makeList.length > 0){M.L.buildPriority = makeList}
        if(makeList.length == 0 && (i <= priorityConstruction.length)){
            i += 1;prioritize()}}
},
findDroppedEnergy: function(){
    M.L.droppedEnergy = Game.flags['Flag1'].room.lookForAtArea(
        RESOURCE_ENERGY,0,39,20,49,{
            asArray:true}).filter(function(element,index,array){
            return(element.energy.amount > 50)});
},
upgradeRampart: function(creep){
    let tempList = Game.flags['Flag1'].room.find(FIND_STRUCTURES,{filter: (structure) =>
        {return (structure.structureType == STRUCTURE_RAMPART && structure.hits <= M.V.rampartPrimaryLimit)}})
    //if(tempList.length){if(creep.repair(tempList[0]) == ERR_NOT_IN_RANGE){creep.moveTo(tempList[0])}}
    if(tempList.length){return tempList}
},
upgradeBlockade: function(creep,inputList){
	if(inputList.length){if(creep.repair(inputList[0]) == ERR_NOT_IN_RANGE){creep.moveTo(inputList[0])}}
},
}
module.exports = mgmt
