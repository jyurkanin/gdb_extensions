import sys
import gdb
import matplotlib.pyplot as plt
import numpy as np
import math

def vector_to_list(std_vector):
    out_list = []
    value_reference = std_vector['_M_impl']['_M_start']
    while value_reference != std_vector['_M_impl']['_M_finish']:
        out_list.append(value_reference.dereference())
        value_reference += 1
    
    return out_list

# This returns the underlying type of an optional
# For example, for std::optional<pc::LonDistTimeEnvelope> this will return
# a token of type std::_Optional_payload<pc::LonDistTimeEnvelope, false, false>::_Stored_type
# Which is just an alias for pc::LonDistTimeEnvelope
# I have no idea what happens if you pass std::nullopt into this, dont do that.
def unwrap_optional(optional):
    return optional["_M_payload"]["_M_payload"]

# todo: dereference raw and shared pointers in here too
def get_value(token):
    if("std::optional" in token.type.name):
        return unwrap_optional(token)
    else:
        return token # no dereferencing necessary
    

class PlotBreak(gdb.Breakpoint):
    def __init__(self, spec, arg):
        super(PlotBreak, self).__init__(spec, type=gdb.BP_BREAKPOINT)
        self.silent = True # This prevents anything from being printed when breakpoint is hit
        self.spec = spec
        self.var = arg
        
        plt.ion() # Show figures immediately without calling show()
        self.fig, self.ax = plt.subplots()
        self.vec = []
        self.ax.set_title(self.var)
        
    def stop(self):
        tk = gdb.parse_and_eval(self.var)
        tk = get_value(tk)
        self.vec.append(tk)
        
        line, = self.ax.plot(self.vec, "b") # blue is my favorite color
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        line.remove()
        
        

class PlotVar(gdb.Command):
    def __init__(self):
        super(PlotVar, self).__init__("plotVar", gdb.COMMAND_SUPPORT, gdb.COMPLETE_SYMBOL)

    def checkInput(self, tokens):
        usage = "plotVar <location> <expression>"
        if not(len(tokens) == 2):
            print(usage)
            return False

        return True

    def invoke(self, arg, from_tty):
        tokens = arg.split(' ')
        
        if not(self.checkInput(tokens)):
            return
        
        PlotBreak(tokens[0], tokens[1])

PlotVar()
