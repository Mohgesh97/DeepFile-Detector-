from FileDetector import FileDetector
from FileRecover import file_recover 
import sys
import hashlib
from PyQt5.QtWidgets import QApplication , QWidget ,QPushButton,QLabel,QTextEdit,QVBoxLayout,QFileDialog,QMessageBox,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer


class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeepFile Detector")
        self.setGeometry(200,200,600,500)
        self.setFixedSize(831,474)
        self.setWindowIcon(QIcon('icon.ico'))
        self.uiSetup()
    
    def uiSetup(self):


        ##GUI Elments buttons

        self.file_upload= QPushButton("Upload file")
        self.download_report_button=QPushButton("Download report")
        self.recover_file_button=QPushButton("Recover file")
        self.hash_calculator=QPushButton("Hash value of recovered file")



         #text field and label
        self.Result_label=QLabel("Detected file type:")
        self.Result_text=QTextEdit()
        self.Result_text.setReadOnly(True)
       

        ##layout 
        Layout1=QHBoxLayout()
        Layout1.addWidget(self.file_upload)
        Layout1.addWidget(self.download_report_button)

        Layout2=QHBoxLayout()
        Layout2.addWidget(self.recover_file_button)
        Layout2.addWidget(self.hash_calculator)


        layout=QVBoxLayout()
        layout.addLayout(Layout1)
        layout.addWidget(self.Result_label)
        layout.addWidget(self.Result_text)
        layout.addLayout(Layout2)
        self.setLayout(layout)


        ##binding Buttons

        self.file_upload.clicked.connect(self.file_select)
        self.download_report_button.clicked.connect(self.report)
        self.recover_file_button.clicked.connect(self.recover)
        self.hash_calculator.clicked.connect(self.hashing)
        ##binding style change 
        self.Result_text.textChanged.connect(self.file_type_changed)
        
       
            
        ##style sheet 
        style= "QWidget{background-color:#f5f7fa; font-family:Arial,sans-serif; font-size:14 px; color:#333333;}"
        style += "QLabel{font-weight:bold; margin-bottom:6 px; }"
        style +="QPushButton{background-color:#007BFF; color:white ; border:none; padding:12px 20px; border-radius:15px; font-size:12px; font-weight:bold;}"
        style +="QPushButton:hover{background-color:#0056b3;}"
        style +="QPushButton:pressed{background-color:#004080;}"
        style +="QTextEdit{background-color:white; border: 1px solid #cccccc; border-radius:10px; padding:8 px;}"
        style +="QLineEdit{background-color:yellow; border: 1px solid #cccccc; border-radius:8px; padding:4 px;}"
        

        self.setStyleSheet(style)
        
    

    

        self.FileCassifier = None
        self.report_text= ""     
      ##to change style each time a file uploaded 
    def file_type_changed(self):
        self.Result_text.setStyleSheet("QTextEdit{ color:#e677ff; border: 4px solid #007BFF; border-radius:8px; padding:8 px; font-size:20 px;}")
        QTimer.singleShot(800,self.rest_QTextEdit)
    def rest_QTextEdit(self):
        self.Result_text.setStyleSheet("QTextEdit{background-color:white; border: 1px solid #cccccc; border-radius:10px; padding:8 px;}")

    def file_select(self):
        file_path ,_=QFileDialog.getOpenFileName(self,"Select File","","All Files(*)")
        if not file_path:
            return
        
        ##file detect
        self.FileCassifier= FileDetector(file_path)
        self.FileCassifier.File_Classify()
        self.report_text= self.FileCassifier.detection_Report()

        ##disply result 
        if self.FileCassifier.officeType:
            detected_file=self.FileCassifier.officeType
        else:
            detected_file=self.FileCassifier.orginaFilel_Type

        self.Result_text.setText(f"Detected file:{detected_file}")

    def report(self):
        if not self.report_text:
            QMessageBox.warning(self,"no report yet" ,"upload file please")
            return
        report_path,_=QFileDialog.getSaveFileName(self,"save Report","fileReport.txt","Text file(*txt)")

        if report_path:
            with open(report_path,"w",encoding="utf-8") as report :
                report.write(self.report_text)
                QMessageBox.information(self,"saved", "report of analysis saved successfully ")
    

    def recover(self):
        if not self.FileCassifier:
            QMessageBox.warning(self,"file not found","Please scan first")
            return
        filePath=self.FileCassifier.filePath
        DetectedFile=self.FileCassifier.orginaFilel_Type

        recoveredFile=None

        if DetectedFile =="PDF":
            recoveredFile=file_recover.pdf_recover(filePath)
        elif DetectedFile =="JPEG":
            recoveredFile = file_recover.jpeg_recover(filePath)
        elif DetectedFile =="PNG":
            recoveredFile= file_recover.png_recover(filePath)
        elif DetectedFile == "GIF":
            recoveredFile= file_recover.Gif_recover(filePath)
        elif DetectedFile =="office":
            recoveredFile=file_recover.office_recover(filePath,self.FileCassifier.officeType)
        if recoveredFile:
            ##store path of recovered file 
            self.new_filepath=recoveredFile
            QMessageBox.information(self,"recovery done!",f"file saved at :{recoveredFile}")
        else:
            QMessageBox.critical(self ,"failed","failed to recover file")

    

    def hashing (self):
        if not self.FileCassifier:
            QMessageBox.warning(self,"file not found","scan a file first")
            return
        
        try:
            with open(self.new_filepath,"rb")as file:
                rec_file=file.read()

            md5= hashlib.md5(rec_file).hexdigest()
            sha1=hashlib.sha1(rec_file).hexdigest()
            sha256=hashlib.sha256(rec_file).hexdigest()

            #display result in Qtext
            self.Result_text.append("Hash values of recovered files")
            self.Result_text.append(f"md5:{md5}")
            self.Result_text.append(f"SHA1:{sha1}")
            self.Result_text.append(f"sha256{sha256}")
        except Exception as e:
            QMessageBox.critical(self,"EROR",f"hash calcution failed!:\n{str(e)}")


        

if __name__ =="__main__":
    app=QApplication(sys.argv)
    window=MainGUI()
    window.setWindowIcon(QIcon('icon.ico'))
    window.show()
    sys.exit(app.exec_())

