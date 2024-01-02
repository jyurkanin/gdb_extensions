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

def get_value(token):
    if("std::optional" in token.type.name):
        return unwrap_optional(token)
    else:
        return token # no dereferencing necessary
    

class plotData(gdb.Command):
    """Plot std::vectors of primitive types"""
    def __init__(self):
        super(plotData, self).__init__("plotData", gdb.COMMAND_SUPPORT, gdb.COMPLETE_SYMBOL)

    # Convert the std vector to a python list
    def plotVector(self, std_vector):
        p_vec = vector_to_list(std_vector)
        plt.plot(p_vec)
        
    def invoke(self, arg, from_tty):
        frame = gdb.selected_frame()
        tokens = arg.split(' ')

        vectors_to_plot = {}

        for i in range(len(tokens)):
            token = tokens[i]
            tk = gdb.parse_and_eval(token)
            tk = get_value(tk)

            if not(tk.type.name in vectors_to_plot.keys()):
                vectors_to_plot[tk.type.name] = []

            vectors_to_plot[tk.type.name].append(tk)

        vector_names = vectors_to_plot.keys()
        
        if any(["std::vector" in name for name in vector_names]):
            # This could be a list of lists of std::vectors with different template types
            std_vectors = [vectors_to_plot[name] for name in vector_names if "std::vector" in name]

            # Flatten all std::vector's into 1 big list. So this
            # list could potentially contain different types, which
            # could be bad if they are not primitive, I thnk.
            flat_std_vectors = []
            [flat_std_vectors.extend(vector) for vector in std_vectors]
            
            for vector in flat_std_vectors:
                self.plotVector(vector)
        
        plt.tight_layout()
        plt.show()

plotData()
