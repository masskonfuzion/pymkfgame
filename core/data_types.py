#############################################################################
# Copyright 2016 Mass KonFuzion
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#############################################################################

class DataWrapper(object):
    ''' A wrapper class to contain an immutable object. The purpose is to allow
        a program to track a reference to an object (most importantly an immutable
        object)

        For now, we'll keep this extra-stupidly simple. We will allow self.data
        to be literally anything.
    '''
    def __init__(self, default_value=None):
        self.data = default_value

    def __getitem__(self, keyName):
        ''' Mimic dict class __getitem__

            Note: really, the only key name that will work is "data"
        '''
        if keyName == "data":
            return self.data
        else:
            raise Exception("DataWrapper class only supports the key name, \"data\"")

    def __setitem__(self, keyName, value):
        ''' Mimic dict class __setitem__

            Note: really, the only key name that will work is "data"
        '''
        if keyName == "data":
            self.data = value
        else:
            raise Exception("DataWrapper class only supports the key name, \"data\"")

