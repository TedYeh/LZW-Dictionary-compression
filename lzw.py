import os
import struct
import sys

# the best compression ratio is 2.67XX 
# taking the input file and the number of bits from command line
# defining the maximum table size
# opening the input file
# reading the input file and storing the file data into data variable

class LZW:
    def __init__(self,filename):
        self.filename = filename
        self.f = open(self.filename+".txt",encoding='UTF-8')
        self.d = list(set(self.f.read())) 
  
    def compress(self):
        n = 16              
        maximum_table_size = pow(2,int(n))      
        file = open(self.filename+".txt",encoding='UTF-8')   
        data = file.read()             
        dic = list(set(data))   
        # Building and initializing the dictionary.
        dictionary_size = len(dic)                   
        dictionary = {dic[i]: i for i in range(dictionary_size)}    
        string = ""             # String is null.
        compressed_data = []    # variable to store the compressed data.
       
        # iterating through the input symbols.
        # LZW Compression algorithm
        for symbol in data:                     
            string_plus_symbol = string + symbol # get input symbol.
            if string_plus_symbol in dictionary: 
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if(len(dictionary) <= maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol
        print(dictionary)
        if string in dictionary:
            compressed_data.append(dictionary[string])
        # storing the compressed string into a file (byte-wise).
        output_file = open(self.filename+"_lzw.bin", "wb")
        for data in compressed_data:
            output_file.write(struct.pack('>H',int(data)))
        output_file.close()
        file.close()
    
    def decompress(self):
        file = open(self.filename+"_lzw.bin", "rb")
        compressed_data = []
        next_code = len(self.d)
        decompressed_data = ""
        string = ""
        
        # Reading the compressed file.
        while True:
            rec = file.read(2)        
            if len(rec) != 2:
                break
            (data, ) = struct.unpack('>H', rec)
            compressed_data.append(data)
        # Building and initializing the dictionary.
        dictionary_size = next_code
        dictionary = dict([(x, self.d[x]) for x in range(dictionary_size)])
        # iterating through the codes.
        # LZW Decompression algorithm
        for code in compressed_data:
            if not (code in dictionary):
                dictionary[code] = string + (string[0])
            decompressed_data += dictionary[code]
            if not(len(string) == 0):
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]
        
        # storing the decompressed string into a file.
        output_file = open(self.filename + "_decoded.txt" , "w",encoding='UTF-8')
        for data in decompressed_data:
            output_file.write(data)           
        output_file.close()
        file.close()
        
    # Check the orignal file is same as decompressed file
    def check_same(self):
        f1, f2 = open(self.filename+".txt",encoding='UTF-8'), open(self.filename+"_decoded.txt",encoding='UTF-8') 
        s1, s2 = f1.read(), f2.read()
        return s1 in s2
        
    #Get file size  
    def get_file_size(self,name):
        return os.path.getsize(str(self.filename+name))
       
    #Get compress ratio    
    def get_ratio(self):    
        after = self.get_file_size("_lzw.bin")
        before = self.get_file_size(".txt")
        return float(before/after)
    
    def get_percentage(self):    
        after = self.get_file_size("_lzw.bin")
        before = self.get_file_size(".txt")
        return float(after/before)
        
if __name__ == "__main__":
    filename = sys.argv
    com = LZW(str(filename[1]))
    com.compress()
    com.decompress()
    if com.check_same():
        print("the decoding is correct！")
    print("before: {0:.3f} KB".format(com.get_file_size(".txt")/1024))
    print("after: {0:.3f} KB".format(com.get_file_size("_lzw.bin")/1024))
    print("the compress ratio is {}%".format(com.get_ratio()))
    print("the compress percentage is {0:.2f}%".format(com.get_percentage()*100))
