import streamlit as st
import streamlit.components.v1 as stc

# testing st.file_uploader functionalities
#uploaded_file = st.file_uploader("Upload Files here",
#								 type=['png', 'jpeg', 'pdf'], 
								 #accept_multiple_files=True
#								)



# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image 
from PyPDF2 import PdfFileReader
import pdfplumber
#from frontend import * 
#import fitz  # this is pymupdf

# define pdf reader functions
def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

def read_pdf_with_pdfplumber(file):
	with pdfplumber.open(file) as pdf:
		all_page_text = ""
		for page in pdf.pages:
			all_page_text += page.extract_text()
		return all_page_text

# define doc file reader funcyion


# define image file reader function
@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img




#if uploaded_file is not None:
#	
#	file_details = {"FileName":uploaded_file.name,
#    			    "FileType":uploaded_file.type, 
#    			    "FileSize":uploaded_file.size
#    			    }
#
#	st.success('PyPDF2 function on action:')
#	res = read_pdf(uploaded_file)
#	st.write(res)

#	st.info('pdfplumber function on action:')
#	result = read_pdf_with_pdfplumber(uploaded_file)
#	st.write(result)

##################
def main():
	st.title("File Uploader & Text Extracter")

	menu = ["Image","Dataset","DocumentFiles","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Image":
		st.subheader("Image")
		image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
		if st.button("Process"):
			if image_file is not None:
			
				# To See Details
				#st.write(type(image_file))
				#st.write(dir(image_file))
				file_details = {"Filename":image_file.name,
								"FileType":image_file.type,
								"FileSize":image_file.size
								}
				st.write(file_details)

				img = load_image(image_file)
				st.image(img,width=250)


	elif choice == "Dataset":
		st.subheader("Load Dataset")
		data_file = st.file_uploader("Upload CSV",type=['csv', 'txt','xlsx'])
		if st.button("Process"):
			if data_file is not None:
				if data_file.type == "text/csv":
					file_details = {"Filename":data_file.name,
									"FileType":data_file.type,
									"FileSize":data_file.size
									}
					st.write(file_details)

					df = pd.read_csv(data_file)
					st.dataframe(df)

				elif data_file.type == "text/plain":
					file_details = {"Filename":data_file.name,
					                "FileType":data_file.type,
					                "FileSize":data_file.size
					                }
					st.write(file_details)

					df = pd.read_csv(data_file, delimiter='\t')
					st.dataframe(df)

				else:
					file_details = {"Filename":data_file.name,
					                "FileType":data_file.type,
					                "FileSize":data_file.size
					                }
					st.write(file_details)
					df = pd.read_excel(data_file)
					st.dataframe(df)



	elif choice == "DocumentFiles":
		st.subheader("Load Document Files")
		docx_file = st.file_uploader("Upload File",type=['txt', 'docx', 'pdf'])
		if st.button("Process"):
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,
								"FileType":docx_file.type,
								"FileSize":docx_file.size
								}
				st.write(file_details)

				# Check File Type
				if docx_file.type == "text/plain":
					# raw_text = docx_file.read() # read as bytes
					# st.write(raw_text)
					# st.text(raw_text) # fails
					st.text(str(docx_file.read(), "utf-8")) # empty
					raw_text = str(docx_file.read(),"utf-8") # works with st.text and st.write,used for futher processing
					# st.text(raw_text) # Works
					st.write(raw_text) # works
				elif docx_file.type == "application/pdf":
					# raw_text = read_pdf(docx_file) # not doing nicer than pdfplumber but works
					# st.write(raw_text)
					try:
						#with pdfplumber.open(docx_file) as pdf:
						#    page = pdf.pages[0]
						#    st.write(page.extract_text())
						st.write(read_pdf_with_pdfplumber(docx_file))
					except:
						st.write("None")
					    
					
				elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
				# Use the right file processor ( Docx,Docx2Text,etc)
					raw_text = docx2txt.process(docx_file) # Parse in the uploadFile Class directory
					st.write(raw_text)

	else:
		st.subheader("About")
		st.info("Built with Streamlit")
		st.success("Elhadji Ngom @stagiare data scientist au sein de la DAI à OIF")
		st.text("School: Data ScienceTech Institute, copyright Juin 2022")



if __name__ == '__main__':
	main()
