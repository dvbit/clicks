from xml.dom.minidom import Entity
import hassapi as hass
from datetime import time, datetime


class clicks(hass.Hass):

    def initialize(self):
        self.log('initializing Clicks...')
        self.clickentities = list(dict(self.args.get('switches', None)).keys())
        self.maxtime = dict(self.args.get('switches', None))
        self.log("self maxtime {}".format(self.maxtime))
        self.entityclicks = dict(self.args.get('switches', None))
        self.log("self entityclicks {}".format(self.entityclicks))

        for clickentity in self.clickentities:
            self.log("Registering Entity {}".format(clickentity))
            self.log("Maxtime  {}".format(self.maxtime[clickentity]))
            self.set_state(clickentity, attributes={ "clicks": 'None' })
            self.entityclicks[clickentity] = 0
            self.listen_state(self.listenclicks, clickentity)
        self.log("self entityclicks {}".format(self.entityclicks))

    def listenclicks(self, entity, attribute, old, new, kwargs):            
        self.log("CB1 Entity {}".format(entity))
        self.log("CB2 EntityClicks {}".format(self.entityclicks[entity]))
        if self.entityclicks[entity] == 0:
            self.entityclicks[entity] = 1
            self.log("Set CB for Entity {} in  {}".format(entity, self.maxtime[entity]))
            self.run_in(self.clickcount, self.maxtime[entity], myentity = entity)
            
        else:
            self.entityclicks[entity] = self.entityclicks[entity] + 1
        self.log("CB3 Entity {} Clicks {}".format(entity,self.entityclicks[entity]))

    def clickcount(self, myentity):
        self.log("CB Entityclicks {} ".format(self.entityclicks))
        self.log("CB MyEntity {} ".format(myentity))
        self.log("Final Clicks {}".format(self.entityclicks[myentity["myentity"]]))
        self.set_state(myentity["myentity"], attributes={ "clicks": self.entityclicks[myentity["myentity"]] })
        self.fire_event("clicks", entity=myentity["myentity"],clicks=self.entityclicks[myentity["myentity"])
        self.entityclicks[myentity["myentity"]] = 0
