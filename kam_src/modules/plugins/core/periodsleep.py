
from modules.plugins.core.base import CoreBase

import time

class PeriodSleep(CoreBase):
	CONFIG_NAME = "global"
	CONFIG_ITEM_PERIOD = "period"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debuggers"]
		self._log = data_dict["logs"]
		self._last_run = time.clock_gettime(time.CLOCK_MONOTONIC)


	def _execute(self):
		now = time.clock_gettime(time.CLOCK_MONOTONIC)
		delta = now - self._last_run
		time_to_sleep = self._sleep - delta

		if self._debug:
			self._debug.log(self._debug.TYPE_EXECUTE, self,\
			            "time_to_sleep", time_to_sleep, "", "")

		if time_to_sleep > 0:
			time.sleep(time_to_sleep)

		self._last_run = time.clock_gettime(time.CLOCK_MONOTONIC)

	def loadConfig(self, config):
		err_value = ""
		section = config[self.CONFIG_NAME]
		if section:
			try:
				sleep = int(section.get(self.CONFIG_ITEM_PERIOD))
			except Exception as e:
				err_value = str(e)
				sleep = 0
		else:
			sleep = None

		if sleep != None and sleep > 0:
			self._sleep = sleep
			self._enable()
		else:
			self._disable()

		if self._log:
			if sleep == None:
				self._log.log(self,\
				              "No section [global] found to load the period from!")
			elif sleep == 0:
				self._log.log(self,\
				              "The config contains an invalid vlaue for [global] -> period. Please enter an integer larger than 0")
			else:
				self._log.log(self,\
				              "Config loaded, period time = {0} seconds".format(self._sleep))

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self,\
					self.CONFIG_ITEM_PERIOD, sleep,\
					err_value, self.isEnabled())

def createInstance(data_dict):
	return PeriodSleep(data_dict)

