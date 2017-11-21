import network
#import heuristic
import pickle
import sys

OUT_FILENAME = 'graph.pickle'

#Main method
def main():
    
    #Generate network
    NET_SIZE = 2000

    netData = network.create(NET_SIZE)

    #Generate all heuristics
    heuristics = {}
    #heuristics['heuristic A'] = heuristic.A(netData)

    #Open output file
    outfile = open(OUT_FILENAME,'wb')

    #Write network and heuristics to output file
    pickle.dump({
        'network' : netData['network'],
        'heuristics' : heuristics
    },outfile)

    #Close output file
    outfile.close()

    #For testing purposes
    print(netData['network'])

main()