
import logging

class Log(object):
    level_set = False
    
    @staticmethod
    def set_loglevel(loglevel):
        logging.getLogger().setLevel(loglevel)
        logging.info("Set loglevel to %d" % loglevel)

if not Log.level_set:
    level = logging.INFO
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(module)s.%(funcName)s(): %(message)s',
                        level=level)
    logging.info("Global logger initialised with loglevel %d" % level)
    Log.level_set = True