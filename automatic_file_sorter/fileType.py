import PyPDF2
from pathlib import Path
from google.cloud import language_v2
import requests
import re
import logging

class FileType():
    #common types of extensions for files
    images_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.psd', '.raw', '.heif', '.heic', '.indd', '.ai', '.svg', '.eps']
    videos_extensions = ['.mp4', '.mov', '.wmv', '.flv', '.avi', '.mkv', '.webm', '.mpeg', '.mpg', '.m4v', '.3gp', '.f4v', '.ts', '.m2ts', '.mts', '.vob']
    microsoft_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.mdb', '.accdb', '.pub', '.vsd', '.vsdx', '.xps']
    audios_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma']
    coding_extensions = ['.py', '.java', '.js', '.html', '.css', '.c', '.cpp', '.cs', '.php', '.rb', '.swift', '.go', '.ts', '.sql', '.sh', '.bat', '.pl', '.lua', '.r', '.kt', '.scala']
    #common keywords for category of pdf files 
    file_keywords_dict = {
    'assignments': ['homework', 'assignment', 'assignments', 'worksheet', 'workbook', 'homeworks', 'project', 'projects', 'lab', 'labs', 'report', 'reports'],
    'lecture_materials': ['lecture', 'lectures', 'notes', 'slides', 'handout', 'handouts', 'presentation', 'presentations'],
    'research_materials': ['paper', 'papers', 'article', 'articles', 'journal', 'journals', 'research', 'study', 'studies', 'educational','education', 'academic'],
    'personal_documents': ['resume', 'cv', 'cover_letter', 'application', 'applications', 'form', 'forms', 'document', 'documents','jobs','job'],
    'miscellaneous_files': ['misc', 'general', 'others', 'extra', 'additional', 'various'],
    'math': ['math', 'mathematics', 'algebra', 'calculus', 'stochastic', 'geometry'],
    'computer_science': ['data structures', 'algorithms', 'data', 'computers', 'computer']
    }

    # Strips the categores into an array of words for the computer to compare to the file keywords dict
    def process_category(category):
        clean_category = category.lstrip('/').lower()
        words = re.split(r'[/ &]+', clean_category)
        words = [word for word in words if word]
        return words

    # url = 'https://language.googleapis.com/v2/documents:classifyText'


    # Create a path for the file to be sorted to
    def create_path(group_name):
        path_name = "/Users/'YOUR USER NAME HERE'/'LOCATION ON PC'/" + group_name
        path = Path(path_name)
        return path
    
    # This organizes the file bases on its filetype, and if it is a pdf, organizes it based on google cloulds characterization of it
    @classmethod
    def return_type(cls,file_path):
        suffix = file_path.suffix

        # if it is a pdf, it starts the google clould api to catgeorize the file
        if suffix == '.pdf':
            # google authenication: export GOOGLE_APPLICATION_CREDENTIALS= "YOUR JSON TOKEN FILE HERE" 
            reader = PyPDF2.PdfReader(file_path)
            num_pages = len(reader.pages)
            if num_pages >= 200:
                return "/Users/noahjaskiewicz/Desktop/Textbooks"
            text = ''
            for page in range(num_pages):
                text += reader.pages[page].extract_text()
                if len(text) >= 950:
                    break
            text = text[:950]
            logging.info(f"Attempting to contact Google")
            client = language_v2.LanguageServiceClient()
            document = language_v2.Document(
                content = text, type_ = language_v2.Document.Type.PLAIN_TEXT
            )
            response = client.classify_text(request={"document": document})
            catergoies = response.categories
            for category in catergoies:
                logging.info(f"category is {category.name} with {category.confidence} category confidence")
                if category.confidence >= .15:
                    words = FileType.process_category(category.name)
                    logging.info(f"The keywords are {words}")
                    for keyWord in FileType.file_keywords_dict:
                        for word in words:
                            if word in FileType.file_keywords_dict[keyWord]:
                                path = FileType.create_path(keyWord)
                                return path
            path = FileType.create_path("Misc")
            return path
        elif suffix in FileType.images_extensions:
            path = FileType.create_path("Images")
            return path
        elif suffix in FileType.audios_extensions:
            path = FileType.create_path("Audios")
            return path
        elif suffix in FileType.videos_extensions:
            path = FileType.create_path("Videos")
            return path
        elif suffix in FileType.coding_extensions:
            path = FileType.create_path("ComputerScience")
            return path
        elif suffix == '.zip':
            path = FileType.create_path("Zip")
            return path
        elif suffix in FileType.microsoft_extensions:
            path = FileType.create_path("MicrosoftFiles")
            return path
        else:
            path = FileType.create_path("Misc")
            return path