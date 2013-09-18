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
    def info(message):
        logging.info(message)
        
    @staticmethod
    def debug(message):
        logging.debug(message)
        
    @staticmethod
    def set_loglevel(loglevel):
        logging.getLogger().setLevel(loglevel)

if not Log.level_set:
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(module)s.%(funcName)s() \"%(message)s\"',
                        level=logging.INFO)
    logging.info("Global logger initialised")
    Log.level_set = True