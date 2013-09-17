"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""

class PBSParameters(object):
    def __init__(self, foldername="", job_name_base="job_", \
                 max_walltime=3600, nodes=1, memory=1):
        self.foldername = foldername
        self.job_name_base = job_name_base
        self.max_walltime = max_walltime
        self.nodes = nodes
        self.memory = memory
