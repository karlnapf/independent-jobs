"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
"""
from results.JobResult import JobResult

class ScalarResult(JobResult):
    def __init__(self, result):
        JobResult.__init__(self)
        self.result = result
    
