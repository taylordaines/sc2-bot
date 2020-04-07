import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, REFINERY, BARRACKS, MARINE, REACTOR


class TayBot(sc2.BotAI):
    async def on_step(self, iteration):
        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_workers() 
        await self.build_supplydepot()
        await self.build_refinery()
        await self.build_barracks()
        await self.build_reactor()
        await self.build_marine()
       
        

    async def build_workers(self):
    	for cc in self.units(COMMANDCENTER).ready.noqueue:
    		 if self.can_afford(SCV) and cc.surplus_harvesters < 0:
    		 	await self.do(cc.train(SCV))

    async def build_supplydepot(self):
    	if self.supply_left < 8 and not self.already_pending(SUPPLYDEPOT) and self.supply_cap < 200:
    		ccs = self.units(COMMANDCENTER).ready
    		if ccs.exists:
    			if self.can_afford(SUPPLYDEPOT):
    				await self.build(SUPPLYDEPOT, near=ccs.first)

    async def build_refinery(self):
    	for cc in self.units(COMMANDCENTER).ready:
    		vespenes = self.state.vespene_geyser.closer_than(15.0, cc)
    		for vespene in vespenes:
    			if not self.can_afford(REFINERY):
    				break
    			worker = self.select_build_worker(vespene.position)
    			if worker is None:
    				break
    			if not self.units(REFINERY).closer_than(1.0,vespene).exists:
    				await self.do(worker.build(REFINERY, vespene))

    async def build_barracks(self):
    	for cc in self.units(COMMANDCENTER).ready:
    		if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS) and self.units(BARRACKS).amount < 2:
    			worker = self.select_build_worker(cc.position)
    			if worker is not None:
    				build_location = await self.find_placement(BARRACKS, cc.position, placement_step=4)
    				await self.do(worker.build(BARRACKS, closer_than(15.0, cc)))

    async def build_marine(self):
        for cc in self.units(BARRACKS).ready.noqueue:
             if self.can_afford(MARINE): 
                await self.do(cc.train(MARINE))

    async def build_reactor(self):
        for cc in self.units(BARRACKS).ready.noqueue:
            if not self.already_pending(REACTOR): 
                if has_add_on(self.units(REACTOR)):
                    break
                if self.units(BARRACKS).amount > 1 and self.units(BARRACKS).amount < 2 :
                    if self.can_afford(REACTOR):
                        await self.build(REACTOR, closer_than(15.0, cc))

    				







run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, TayBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True) 