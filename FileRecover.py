from FileDetector import FileDetector
import os 
import struct
import zipfile
import tempfile
import shutil

class file_recover:
    @staticmethod
    def pdf_recover(filePath):
        try:
            with open(filePath,"rb")as file:
                data= file.read()
        except Exception as e :
            print(f"File read error:{e}")

            ##PDF header signature
        PdfHeader= b"%PDF-1.4\n"
        PdfFooter= b"%%EOF"

            ##geting lenght of header and footer
        PdfHeader_len=len(PdfHeader)
        PdfFooter_len=len(PdfFooter)

            ##adding header to new file
        Pdf_recovered= PdfHeader + data[PdfHeader_len:]
            ##adding both header and footer if footer is tampered as well
        if not Pdf_recovered.endswith(PdfFooter):
            Pdf_recovered=Pdf_recovered[0:len(data)-PdfFooter_len] + PdfFooter

            #writing new file recoverd     

        new_pdf= os.path.splitext(filePath)[0] +"-recoveredOrginal"+ FileDetector.Map_extentions.get("PDF",".pdf")
        try:
            with open(new_pdf,"wb") as file:
                    file.write(Pdf_recovered)
        except Exception as e :
            print(f"File read error:{e}")
            return None
        return new_pdf
        


    def jpeg_recover(filePath):
        try:
            with open(filePath,"rb")as file:
                data= file.read()
        except Exception as e :
            print(f"File read error:{e}")

            ##jpeg header and footer signatures
        JpegHeader= b'\xff\xd8'
        JpegFooter= b'\xff\xd9'

            ##geting lenght of header and footer
        JpegHeader_len=len(JpegHeader)
        JpegFooter_len=len(JpegFooter)

            ##adding header to new file
        Jpeg_recovered= JpegHeader + data[JpegHeader_len:]
            ##adding both header and footer if footer is tampered as well
        if not Jpeg_recovered.endswith(JpegFooter):
            Jpeg_recovered=Jpeg_recovered[0:len(data)-JpegFooter_len] + JpegFooter

            #writing new file recoverd     

        new_Jpeg= os.path.splitext(filePath)[0] +"-recoveredOrginal"+ FileDetector.Map_extentions.get("JPEG",".jpg")
        try:
            with open(new_Jpeg,"wb") as file:
                file.write(Jpeg_recovered)
        except Exception as e :
            print(f"File read error:{e}")
            return None
        return new_Jpeg
        

    
    def png_recover(filePath):

        try:
            with open(filePath,"rb")as file:
                 data= file.read()
        except Exception as e :
            print(f"File read error:{e}")

            ##png header and footer signatures
        PngHeader= b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D'
        PngFooter= b'\x00\x00\x00\x00IEND\xaeB\x60\x82'

            ##geting lenght of header and footer
        PngHeader_len=len(PngHeader)
        PngFooter_len=len(PngFooter)

            ##adding header to new file
        Png_recovered= PngHeader + data[PngHeader_len:]
            ##check if correct footer not found , add the signature  
        if not Png_recovered.endswith(PngFooter):
            Png_recovered=Png_recovered[0:len(data)-PngFooter_len] + PngFooter

            #writing new file recoverd     

        new_png= os.path.splitext(filePath)[0] +"-recoveredOrginal"+ FileDetector.Map_extentions.get("PNG",".png")
        try:
            with open(new_png,"wb") as file:
                    file.write(Png_recovered)
        except Exception as e :
            print(f"File read error:{e}")
            return None
        return new_png
        

    def office_recover(filePath, officeType):

        try:
            with open (filePath,"rb") as file:
                data= file.read()
        except Exception as e:
            print(f"File raed error:{e}")  
            return None      
        
        ##add zip header 
        data= b'PK\x03\x04' + data [4:]
        ##first need to find the central directories entries 
        central_dirctory= b'PK\x01\x02'
        ##searching for all central directories entries with their postions 
        central_dirctory_postions=[]
        pos=0
        while True:
            cdIndex=data.find(central_dirctory,pos)
            if cdIndex == -1:
                break
            central_dirctory_postions.append(cdIndex)
            pos= cdIndex + 1
        if not central_dirctory_postions:
            print("no central directories found ")
            return None
        #the first offset found for central directory
        First_central_directory=central_dirctory_postions[0]
        #offset of last central directory
        Last_central_directory = central_dirctory_postions[-1]
        ##count how many central directories found
        total_of_central_directory= len(central_dirctory_postions)

        #calculate the last central directory entry size , 46 bytes fixed header + 3 variable length
        #  ##extracts the 2 bytes that store the filename lenght
        file_name_lenght= int.from_bytes(data[Last_central_directory+28:Last_central_directory+30],'little')
        ##at offset 30 to 32 to get the lenght of extra feilds like timestamps that  are stored here 
        extraField_lenght=int.from_bytes(data[Last_central_directory+30:Last_central_directory+32],'little')
         ##32 to 34 it containes the lenght of the comment field 
        file_comment_lenght=int.from_bytes(data[Last_central_directory+32:Last_central_directory+34],'little')
        
        Total_lengnt_of_Last_central= 46 + file_name_lenght + extraField_lenght + file_comment_lenght
        ##to get the end offset of last entry by adding offset last entry found at +lenght of the last entry 
        cd_end = Last_central_directory + Total_lengnt_of_Last_central
        ##caluclate the size of the central directory
        cd_size = cd_end - First_central_directory

        #re-construct the EOCD
        eocd_footer = (
            b'PK\x05\x06' +  ##footer signture 
            b'\x00\x00' + 
            b'\x00\x00' +
            struct.pack('<H', total_of_central_directory) + ##total number of entries 
            struct.pack('<H', total_of_central_directory) +
            struct.pack('<I', cd_size) +                   ##size of central directory 
            struct.pack('<I', First_central_directory) +   #the offset where the central directory starts at 
            b'\x00\x00'
        )

        ##remove if any parts of the EOCD  still exists
        
        existing_footer = data.find(b'PK\x05\x06')
        if existing_footer != -1:
            data = data[:existing_footer]
        ##new data with reparied footer EOCD
        reparied_footer=data[:cd_end] + eocd_footer 
        
        
        ##save as an intermediadte zip##
        newZip = os.path.splitext(filePath)[0] + "reparied_temp.zip"
        with open(newZip, "wb") as f:
            f.write(reparied_footer)

        #make a temp dir and exract files from new zip
        temp_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(newZip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        except Exception as e:
            print("connot extract ", e)
            shutil.rmtree(temp_dir)
            return None
    ##build new archive##
        new_archive = os.path.splitext(filePath)[0] + "-recoveredOriginal"
    ## creating a zip archive for the extracted files from temp dir###
        shutil.make_archive(new_archive, 'zip', temp_dir)
    ##maping with correct extention## 
        new_office = new_archive + FileDetector.Map_extentions.get(officeType, ".docx")
        ##rename from .zip to the correct extention##
        os.rename(new_archive + ".zip", new_office)
     ##removing the temp after creating the file## 
        shutil.rmtree(temp_dir)
      ##remove the intermediadte zip###
        if os.path.exists(newZip):
          os.remove(newZip)
        return new_office
    
   # ///////////////////////////////////////////////////////////////////////////////////////
    def Gif_recover(filePath):

        try:
            with open(filePath,"rb")as file:
                data= file.read()
        except Exception as e :
            print(f"File read error:{e}")

            ##GIF header and footer signatures
        GIFHeader= b'\x47\x49\x46\x38\x39\x61'
        GIFFooter= b'\x3B'

            ##geting lenght of header and footer
        GIFHeader_len=len(GIFHeader)
        GIFFooter_len=len(GIFFooter)

            ##adding header to new file
        GIF_recovered= GIFHeader + data[GIFHeader_len:]
            ##adding both header and footer if footer is tampered as well
        if not GIF_recovered.endswith(GIFFooter):
            GIF_recovered=GIF_recovered[0:len(data)-GIFFooter_len] + GIFFooter

            #writing new file recoverd     

        new_GIF= os.path.splitext(filePath)[0] +"-recoveredOrginal"+ FileDetector.Map_extentions.get("GIF",".gif")
        try:
            with open(new_GIF,"wb") as file:
                file.write(GIF_recovered)
        except Exception as e :
            print(f"File read error:{e}")
            return None
        return new_GIF


        







