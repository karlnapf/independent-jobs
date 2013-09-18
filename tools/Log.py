"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
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