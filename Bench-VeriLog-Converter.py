import os
import re
def main():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.bench'):
            invar = []
            outvar = []
            instructions =[]
            wire = []
            with open(filename) as myfile:
                for myline in myfile:
                    if "INPUT" in myline:
                        str = myline.split("(")[1].split(")")[0].rstrip()
                        invar.append(str)
                    if "OUTPUT" in myline:
                        str = myline.split("(")[1].split(")")[0].rstrip()
                        outvar.append(str)
                    if "=" in myline:
                        str1, str2 = myline.split("=")
                        gate, str2a = str2.split("(")
                        instructions.append(gate.lower()+"("+str1+","+str2a.rstrip()+";"+"\n")
                        for w in str2a[:-2].replace(" ","").split(","):
                            if w in wire or w in invar or w in outvar:
                                continue
                            else:
                                wire.append(w)
            FileWrite(filename,invar,outvar,instructions, set(wire))

def FileWrite(filename, invar, outvar, instructions, wire):
    # wires= set(wire)
    iovar = set(invar) & set(outvar)
    inputs =''
    outputs=''
    inouts=''
    ins=''
    wrs=''

    for io in iovar:
        inouts = inouts+str(io)+","
        if(io in invar):
            invar.remove(io)
        if(io in outvar):
            outvar.remove(io)
    for o in outvar:
        outputs = outputs+o+","
    for i in invar:
        inputs = inputs+i+","
    for wi in wire:
        wrs = wrs + wi + ","
    for inst in instructions:
        ins = ins+inst[1:]
    
    
    vname = filename.split(".")[0] + ".v"
    fff= open(vname,"w+")
    module = "module " + filename.split(".")[0] + "\n"
    variables = "(" + inouts + outputs + inputs[:-1] + ");\n\n"
    iovaiables = "inout " + inouts[:-1] + ";\n"
    outvaiables = "output " + outputs[:-1] + ";\n"
    invaiables = "input " + inputs[:-1] + ";\n"
    wireVar = "wire " + wrs[:-1] + ";\n\n"

    fff.write(module + variables + iovaiables + outvaiables + invaiables + wireVar + ins + "endmodule")
    fff.close()
    print("converted "+filename+" to "+vname)

if __name__=="__main__":
    main()
