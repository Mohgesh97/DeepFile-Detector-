class OfficeScanner:
    officeInternalSignatures={"wordDocument":b"word/document.xml",
                              "powerpointPPTX":b"ppt/presentation.xml",
                              "ExcelFiles": b"xl/workbook.xml"
                              }
    def scan(self,data):
        for fileType,signature in self.officeInternalSignatures.items():
            offset=data.find(signature)
            if offset != -1:
                return 100 ,{"type":fileType,"offset":offset}
        return 0, None

class PdfScanner:
    def scan(self,data):
    #internal markers 
     InternalSignatures = {
       "catalog": b'\x2F\x54\x79\x70\x65\x20\x2F\x43\x61\x74\x61\x6C\x6F\x67',
        "pages" : b'\x2F\x54\x79\x70\x65\x20\x2F\x50\x61\x67\x65\x73',
        "crossRefrance": b'\x78\x72\x65\x66' 
    }
     
     catalogSearch= data.find(InternalSignatures["catalog"])
     pageSearch=data.find(InternalSignatures["pages"])
     crossRefrance= data.find(InternalSignatures["crossRefrance"])

     #using a scoring system for each signature identified 
     score=0
     if catalogSearch != -1:
         score+=25
     if pageSearch!= -1 :
         score+=25
     if crossRefrance!= -1:
         score+=50

     Offset_of_found_signatures={"catalog":catalogSearch,"pages":pageSearch,"crossRefrance":crossRefrance }
     
     return score,Offset_of_found_signatures

class JpegScanner:
    def scan(self, data):
        internalSignatures = {
        "DQT": b'\xFF\xDB', #Define Quntization Table signature
        "SOF0": b'\xFF\xC0', #baseline start of frame
        "SOF2":b'\xFF\xC2', #Progressive start of frame
        "DHT": b'\xFF\xC4' , #huffman table
        "SOS":b'\xFF\xDA' #Start of scan
    } 

        #SEARCH if any are avilable basline or progressive start of frame
        SOF0Search=data.find(internalSignatures["SOF0"])
        SOF2Search=data.find(internalSignatures["SOF2"])
        if SOF0Search == -1 and SOF2Search == -1:
            startOframe= -1
        elif SOF0Search==-1:
            startOframe=SOF2Search
        elif SOF2Search== -1:
            startOframe=SOF0Search
        else:
            startOframe = min(SOF0Search,SOF2Search)
                #searching for internal markers
        DqtSearch=data.find(internalSignatures["DQT"])
        HuffmanSearch=data.find(internalSignatures["DHT"])
        SOSsearch=data.find(internalSignatures["SOS"])

        foundSignatures={"DQT":DqtSearch ,"SOF":startOframe ,"DHT":HuffmanSearch,"SOS":SOSsearch }

        #ALL must be found in logical oreder in jpeg to be true  DQT<SOF<DHT<SOS
        if -1 in foundSignatures.values():
            return 0 , foundSignatures
        
        if DqtSearch< startOframe <HuffmanSearch< SOSsearch:
            return 100 , foundSignatures
        return 0 , foundSignatures

class PngScanner():
    
    def scan(self,data):
        IhdrSearch= data.find(b'IHDR')
        IdatSearch=data.find(b'IDAT')
        ##stroing offset in dictionary 
        SignaturesPNG= {"IHDR":IhdrSearch , "IDAT":IdatSearch}

        ##detected signatures 
        foundSignatures={}
        if IhdrSearch!= -1:
            foundSignatures["IHDR"]= IhdrSearch
        if IdatSearch != -1:
            foundSignatures["IDAT"]=IdatSearch

        
        ##to reduce false positive both signatures must be detected
        if len(foundSignatures)< 2 :
            return 0 ,SignaturesPNG
        ##validating that both signatures detected are in the correct logical order in a png image
        if "IHDR" in foundSignatures and "IDAT" in foundSignatures:
            if foundSignatures["IHDR"] >= foundSignatures["IDAT"]:
                return 0,SignaturesPNG        
        return 100 ,SignaturesPNG




class GifScanner:
    def scan(self, data):
        graphic_control_extensions = []
        offset = 0
        #iterating through the binary data from offset 0 to search for GCE blocks
        while offset < len(data) - 8:
            if (data[offset] == 0x21 and
                data[offset + 1] == 0xF9 and
                data[offset + 2] == 0x04 and
                data[offset + 7] == 0x00):  # Valid GCE block length and terminator
                graphic_control_extensions.append(offset)
                offset += 8  # once block detected Skip by 8 bytes the length of the GCE block to continue searching  
            else:
                offset += 1

       
        if graphic_control_extensions:
            return 100, {"GCE_Count": len(graphic_control_extensions), "Offsets": graphic_control_extensions}
        else:
            return 0, {"GCE_Count": 0, "Offsets": []}




 




          
          
           



      


