import os 
from FileAnalyze import OfficeScanner
from FileAnalyze import PdfScanner
from FileAnalyze import JpegScanner
from FileAnalyze import PngScanner
from FileAnalyze import GifScanner


class FileDetector:
    Map_extentions ={
        "PDF":".pdf",
        "PNG": ".png",
        "JPEG":".jpg",
        "wordDocument":".docx",
        "powerpointPPTX":".pptx",
        "ExcelFiles":".xlsx",
        "GIF":".gif"
    }
    def __init__(self,filePath):
        ##constuctor
        #store file path
        self.filePath=filePath
        #read binary into memory
        self.data=self.readFile()
        #score of signatures detected
        self.Results={}
        self.orginaFilel_Type=None
        self.officeType= None

    def readFile(self):
        try:
            with open(self.filePath,"rb")as file:
                return file.read()
        except Exception as e :
            print(f"File read error:{e}")


    def File_Classify(self):
        if not self.data:
            return{"error":"No data to read"}
        ##Microsoft office files
        offic_score, office_signatures = OfficeScanner().scan(self.data)
        if offic_score > 0:
         self.Results["office"] = {
        "score": offic_score,
        "signatures": office_signatures }
        else:
         self.Results["office"] = {
        "score": 0,
        "signatures": {}}
         
         ##PDF scanner
        pdf_score ,pdf_signatures = PdfScanner().scan(self.data)
        self.Results["Pdf"]={"score":pdf_score , "signatures":pdf_signatures}
        ##png scanner
        Png_score ,Png_signatures = PngScanner().scan(self.data)
        self.Results["png"] ={"score":Png_score, "signatures":Png_signatures}
        #Gif Scanner
        Gif_score , Gif_signatures= GifScanner().scan(self.data)
        self.Results["GIF"] ={"score":Gif_score,"signatures":Gif_signatures}

        ##JPEG

        Jpeg_score , Jpeg_signatures = JpegScanner().scan(self.data)
        self.Results["jpeg"]={"score":Jpeg_score, "signatures":Jpeg_signatures}

        return self.Results
       
    def detection_Report(self):
        report_file= [ 
            f"File: {self.filePath}" ,
            f"File size:{os.path.getsize(self.filePath)} bytes",
            "*"*50,
            "scan Results: ",
            "Score:0-100",
            "offset location if signature detected",
             "*"*50,
            ]
        
          
        for filetype , result in self.Results.items():
            score=result.get("score",0)
            signatures=result.get ("signatures",{})
            report_file.append(f"\n{filetype}:")
            report_file.append(f"Score:{score}")
            if signatures:
                report_file.append("Details:")
                for key , value in signatures.items():
                    report_file.append(f"{key}:{value}")

##decion on final type 
        
        if "office" in self.Results and self.Results["office"]["score"] == 100:
            self.orginaFilel_Type = "office"
            self.officeType = self.Results["office"]["signatures"].get("type")
            decision = f"The file type detected is a {self.officeType} document."


        elif self.Results.get("Pdf",{}).get("score",0) >= 50:
            self.orginaFilel_Type=  "PDF"
            decision= "The file type detected is a PDF document."

        elif self.Results.get("png",{}).get("score",0)== 100:
            self.orginaFilel_Type= "PNG"
            decision= "The file type detected is a PNG document."

        elif self.Results.get("GIF",{}).get("score",0) == 100: 
            self.orginaFilel_Type= "GIF"
            decision= "The file type detected is a GIF document."
        
        elif self.Results.get("jpeg",{}).get("score",0) == 100:
            self.orginaFilel_Type=  "JPEG"
            decision= "The file type detected is a JPEG document."

        else:
            self.orginaFilel_Type= "unknown"
            decision= "unable to detect document type."
        
        ##disply the true extention
        if self.orginaFilel_Type == "office" and self.officeType in self.Map_extentions:
           extention = self.Map_extentions[self.officeType]
           decision += f"(the orginal extention should be :{extention})"
        elif self.orginaFilel_Type in self.Map_extentions:
            extention = self.Map_extentions[self.orginaFilel_Type]
            decision += f"(the orginal extention should be :{extention})"

        

        ##
        report_file.append("/n"+"-"*50)
        report_file.append("Detected type:" + decision)
      

        return "\n".join(report_file)
    








    


